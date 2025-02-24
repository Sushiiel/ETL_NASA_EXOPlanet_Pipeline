from google.cloud import bigquery

project_id="myproject1-408614"
dataset_id="sample_dataset_2"
table_id="exoplanets_table"
staging_table_id="exoplanets_table_staging"
gcs_uri="gs://us-central1-composer-dev-4-2d9d25ef-bucket/data/nasa_filtered - exoplanets_table.csv"

client=bigquery.Client()
dataset_ref=client.dataset(dataset_id)
try:
    client.get_dataset(dataset_ref)
except Exception:
    print(f"Dataset {dataset_id} not found, creating it...")
    dataset=bigquery.Dataset(dataset_ref)
    dataset.location="US"
    client.create_dataset(dataset,exists_ok=True)

staging_table_ref=dataset_ref.table(staging_table_id)
final_table_ref=dataset_ref.table(table_id)

job_config=bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV,skip_leading_rows=1,field_delimiter=",",autodetect=True,write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

print(f"⏳ Loading data into staging table {staging_table_id}...")
job=client.load_table_from_uri(gcs_uri,staging_table_ref,job_config=job_config)
job.result()
print(f"✅ Data loaded into staging table {staging_table_id}")

query=f"""
    SELECT column_name,data_type 
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS` 
    WHERE table_name='{staging_table_id}'
"""

schema_info=client.query(query).result()
print("📌 Column Data Types in Staging Table:")
for row in schema_info:
    print(f"Column:{row['column_name']},Type:{row['data_type']}")

query=f"""
    SELECT column_name 
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS` 
    WHERE table_name='{staging_table_id}' AND column_name NOT IN ('koi_score','kepid','kepoi_name')
"""
columns=[row["column_name"] for row in client.query(query).result()]
column_str=", ".join([f"SAFE_CAST({col} AS FLOAT64) AS {col}" for col in columns])

query=f"""
    INSERT INTO `{project_id}.{dataset_id}.{table_id}`
    SELECT SAFE_CAST(kepid AS INT64) AS kepid,SAFE_CAST(koi_score AS FLOAT64) AS koi_score,SAFE_CAST(kepoi_name AS STRING) AS kepoi_name,{column_str}
    FROM `{project_id}.{dataset_id}.{staging_table_id}`
"""

try:
    print(f"⏳ Transforming and inserting data into {table_id}...")
    query_job=client.query(query)
    query_job.result()
    print(f"✅ Data successfully transformed and inserted into {table_id}")
except Exception as e:
    print(f"❌ Error during data transformation:{e}")

try:
    client.delete_table(staging_table_ref,not_found_ok=True)
    print(f"🗑️ Staging table {staging_table_id} deleted.")
except Exception as e:
    print(f"⚠️ Error deleting staging table:{e}")
