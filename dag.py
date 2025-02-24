from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

PROJECT_ID="myproject1-408614"
BUCKET_NAME="us-central1-composer-dev-4-2d9d25ef-bucket"
GCS_SCRIPT_PATH="dags/scripts/extract.py"
REGION="us-central1"
DATAFUSION_INSTANCE="datafus-central-1"
PIPELINE_NAME="nasa_ETL_pipeline_31"

default_args={"owner":"airflow","start_date":datetime(2024,2,21),"retries":1,"execution_timeout":timedelta(minutes=15)}

with DAG(dag_id="exoplanet_pipeline_gcs_bash",default_args=default_args,schedule="@daily",catchup=False) as dag:
    run_gcs_script=BashOperator(task_id="run_python_script_gcs",
    bash_command=f"gsutil cp gs://{BUCKET_NAME}/{GCS_SCRIPT_PATH} /tmp/extract.py&&python3 /tmp/extract.py",
    do_xcom_push=False)

    start_pipeline=CloudDataFusionStartPipelineOperator(task_id="start_datafusion_pipeline",
    project_id=PROJECT_ID,
    location=REGION,
    instance_name=DATAFUSION_INSTANCE,
    pipeline_name=PIPELINE_NAME,
    runtime_args={},asynchronous=False)

    run_gcs_script>>start_pipeline
