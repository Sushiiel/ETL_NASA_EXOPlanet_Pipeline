# ETL Pipeline for Exoplanet Data using Google Cloud

## Overview
This project is an ETL (Extract, Transform, Load) pipeline that processes exoplanet data from NASA's Exoplanet Archive API. The pipeline leverages Google Cloud services, including:

- **Apache Airflow** to create a DAG that orchestrates the ETL pipeline, triggering the **GCP Cloud Fusion** pipeline.
- **Cloud Storage Buckets** for storing raw and processed data.
- **Cloud Fusion** for integrating data transformations.
- **Looker Studio** for visualization and analysis.

## Data Source
The dataset is extracted from NASA's Exoplanet Archive API using the following query:

```
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&where=koi_prad<2 and koi_teq>180 and koi_teq<303 and koi_disposition like 'CANDIDATE'
```

## Pipeline Architecture
1. **Extract**: Fetch exoplanet data from the API.
2. **Transform**: Clean and filter the dataset based on criteria.
3. **Load**: Store processed data in Google Cloud Storage.
4. **Analyze**: Visualize insights using Looker Studio.

## Files in this Repository
- `dag.py`: Airflow DAG for orchestrating the ETL process.
- `extract.py`: Python script for data extraction and processing.
- `exoplanets_filtered.csv`: Filtered dataset after transformation.
- `nasa_filtered - exoplanets_table.csv`: Additional dataset for analysis.

## Setup & Execution
### Prerequisites
- Google Cloud SDK installed.
- Python 3.x.
- Required Python libraries (`pandas`, `requests`, `google-cloud-storage`).

### Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/your-repo.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the extraction script:
   ```sh
   python extract.py
   ```
4. Deploy and monitor the DAG in Airflow.
5. Visualize results in Looker Studio.

## Visuals
Below are images illustrating the pipeline execution:

### Cloud Fusion Workflow
![Cloud Fusion](https://raw.githubusercontent.com/Sushiiel/ETL_NASA_EXOPlanet_Pipeline/main/ETL_GCP_Pipeline_4.png)

### Apache Airflow DAG
Apache Airflow is used to create a DAG for orchestrating the ETL pipeline, where it triggers the **GCP Cloud Fusion** pipeline.

![ETL Pipeline](https://raw.githubusercontent.com/Sushiiel/ETL_NASA_EXOPlanet_Pipeline/main/ETL_GCP_Pipeline_1.png)

![ETL Pipeline](https://raw.githubusercontent.com/Sushiiel/ETL_NASA_EXOPlanet_Pipeline/main/ETL_GCP_Pipeline_2.png)

## Author
- **Sushiiel** - [Your GitHub Profile](https://github.com/Sushiiel)
