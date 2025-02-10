from google.cloud import storage
import pandas as pd

# Authenticate with service account
storage_client = storage.Client.from_service_account_json("service_account_file.json")

# Load stock sentiment data
stock_sentiment_df = pd.read_csv("financial_analysis.csv")

# Save DataFrame as CSV locally
csv_filename = "financial_analysis.csv"
stock_sentiment_df.to_csv(csv_filename, index=False)

# Upload to GCS bucket
bucket_name = "yourt-bucket"
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(csv_filename)
blob.upload_from_filename(csv_filename)

print(f"File {csv_filename} uploaded to {bucket_name}.")
