from google.cloud import bigquery

# Authenticate with BigQuery
client = bigquery.Client.from_service_account_json("service_account_file.json")

# Define dataset & table
dataset_id = "finance_sentiment"
table_id = "stock_sentiment"

# Create dataset if not exists
dataset_ref = client.dataset(dataset_id)
try:
    client.get_dataset(dataset_ref)
    print("Dataset exists")
except:
    client.create_dataset(bigquery.Dataset(dataset_ref))
    print("Dataset created")

# Define BigQuery schema
schema = [
    bigquery.SchemaField("Date", "DATE"),
    bigquery.SchemaField("Close", "FLOAT"),
    bigquery.SchemaField("High", "FLOAT"),
    bigquery.SchemaField("Low", "FLOAT"),
    bigquery.SchemaField("Open", "FLOAT"),
    bigquery.SchemaField("Volume", "INTEGER"),
    bigquery.SchemaField("Tweet_Sentiment", "STRING"),
    bigquery.SchemaField("News_Sentiment", "STRING"),
]

# Load CSV from GCS to BigQuery
job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
)
bucket_name = "your-bucket"
csv_filename = "financial_analysis.csv"
gcs_uri = f"gs://{bucket_name}/{csv_filename}"
load_job = client.load_table_from_uri(gcs_uri, f"{dataset_id}.{table_id}", job_config=job_config)
load_job.result()

print(f"Data successfully loaded into {dataset_id}.{table_id}.")
