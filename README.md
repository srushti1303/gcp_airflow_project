# gcp_airflow_project

📌 Project Overview
This project implements an end-to-end real-time financial sentiment analysis and anomaly detection system using Google Cloud Platform (GCP), AI/ML, and NLP. It processes live stock prices, financial news, and tweets to extract sentiment insights and detect unusual market movements (e.g., insider trading, flash crashes).

🚀 Tech Stack Used:
✅ Google Cloud Platform (BigQuery, Cloud Storage, Cloud Composer, Looker Studio)
✅ Airflow (DAGs for automated data ingestion & transformation)
✅ Machine Learning (Isolation Forest, Autoencoders for anomaly detection)
✅ NLP (FinBERT for sentiment analysis, NER for stock symbol extraction)
✅ Pandas, NumPy, Matplotlib, Seaborn (Data Processing & Visualization)

📌 Project Workflow
Step 1: Data Collection & Ingestion

Stock Market Data → Fetched from Yahoo Finance API (Date, Open, Close, High, Low, Volume)
Financial News Data → Extracted from News API (Title, Source, Published Date, Description)
Twitter Data → Fetched from Twitter API (Tweets related to stocks, hashtags, timestamps)
Data is preprocessed and stored in Google Cloud Storage (GCS) before loading into BigQuery.

Step 2: Sentiment Analysis & NLP (AI & Data Science Focus)

FinBERT is used to classify tweets & news into Positive, Negative, Neutral Sentiment.
Named Entity Recognition (NER) extracts stock symbols & company names from text.
The final dataset is stored in BigQuery (finance_sentiment.stock_sentiment).

Step 3: Correlate Sentiment with Stock Prices (SQL in BigQuery)

Aggregated sentiment trends vs. stock price movements using SQL queries in BigQuery.
"Overall Sentiment" column generated to classify market sentiment shifts.

Step 4: Anomaly Detection (Machine Learning Focus)

Isolation Forest & Autoencoder Models detect unusual stock price movements (e.g., pump-and-dump, insider trading).
Cross-checks anomalies with news sentiment.

Step 5: Predictive Modeling (ML-Based Stock Price Forecasting)

Built ML models (LSTM, Random Forest) to predict stock price movements based on past price & sentiment trends.
Step 6: Data Pipeline Automation (Cloud Composer & Airflow DAGs)

Airflow DAG automates:
Data Ingestion (from APIs → GCS → BigQuery)
Sentiment Analysis & Storage
Anomaly Detection & Alerts
Step 7: Visualization (Looker Studio Dashboard)

📊 Visuals Created:
https://lookerstudio.google.com/s/rWNyBg8O7tA

📌 Contributors
👤 Srushti Kamble - LinkedIn | GitHub

📩 Have questions? Reach out! 🚀
