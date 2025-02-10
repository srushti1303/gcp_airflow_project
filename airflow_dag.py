from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

# DAG definition
dag = DAG(
    'finance_sentiment_pipeline',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)

# ✅ Load CSV from GCS to BigQuery
load_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_to_bq',
    bucket='your-bucket',
    source_objects=['financial_analysis.csv'],
    destination_project_dataset_table='table_name',
    write_disposition='WRITE_TRUNCATE',  # Overwrites table daily
    autodetect=True,  # Auto-detect schema
    dag=dag
)

# ✅ Insert Sentiment Analysis results into a new BigQuery table
sentiment_analysis_task = BigQueryInsertJobOperator(
    task_id="run_sentiment_analysis",
    configuration={
        "query": {
            "query": """
                CREATE OR REPLACE TABLE `table_name` AS
                SELECT Date, Close, Open, Volume, 
                       Tweet_Sentiment, News_Sentiment,
                       CASE 
                           WHEN Tweet_Sentiment > 0 AND News_Sentiment > 0 THEN 'Positive'
                           WHEN Tweet_Sentiment < 0 AND News_Sentiment < 0 THEN 'Negative'
                           ELSE 'Neutral'
                       END AS Overall_Sentiment
                FROM `table_name`;
            """,
            "useLegacySql": False
        }
    },
    dag=dag,
)

# ✅ Set task dependencies (Run in sequence)
load_to_bq >> sentiment_analysis_task
