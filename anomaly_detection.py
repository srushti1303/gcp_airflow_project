import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

# Load the dataset
stock_sentiment_df = pd.read_csv("financial_analysis.csv", parse_dates=["Date"])

# Feature Engineering: Compute Daily Stock Returns
stock_sentiment_df["Price_Change"] = stock_sentiment_df["Close"].pct_change()

# Drop NaN values caused by pct_change()
stock_sentiment_df.dropna(inplace=True)

# Select features for anomaly detection
features = ["Price_Change", "Volume", "Tweet_Sentiment", "News_Sentiment"]
data = stock_sentiment_df[features]

# Standardize the data (Important for Isolation Forest & Autoencoder)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Train Isolation Forest
iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
stock_sentiment_df["Anomaly_IF"] = iso_forest.fit_predict(scaled_data)

# Convert anomaly labels (-1 = anomaly, 1 = normal) into binary
stock_sentiment_df["Anomaly_IF"] = stock_sentiment_df["Anomaly_IF"].apply(lambda x: 1 if x == -1 else 0)

print("✅ Isolation Forest Anomalies Detected.")

# Define the Autoencoder Model
input_dim = scaled_data.shape[1]

autoencoder = Sequential([
    Dense(32, activation="relu", input_shape=(input_dim,)),
    Dropout(0.2),
    Dense(16, activation="relu"),
    Dense(8, activation="relu"),
    Dense(16, activation="relu"),
    Dense(32, activation="relu"),
    Dense(input_dim, activation="linear")  # Reconstruct input
])

autoencoder.compile(optimizer=Adam(), loss="mse")

# Train Autoencoder
autoencoder.fit(scaled_data, scaled_data, epochs=50, batch_size=32, shuffle=True)

# Compute Reconstruction Error
reconstructions = autoencoder.predict(scaled_data)
reconstruction_error = np.mean(np.abs(reconstructions - scaled_data), axis=1)

# Set threshold for anomalies (e.g., top 1% highest errors)
threshold = np.percentile(reconstruction_error, 99)

# Flag Anomalies
stock_sentiment_df["Anomaly_AE"] = (reconstruction_error > threshold).astype(int)

print("✅ Autoencoder Anomalies Detected.")

# Filter Anomalies
anomaly_df = stock_sentiment_df[(stock_sentiment_df["Anomaly_IF"] == 1) | (stock_sentiment_df["Anomaly_AE"] == 1)]

# Check correlation with negative sentiment
anomaly_df["High_Negative_Impact"] = ((anomaly_df["Tweet_Sentiment"] < -0.5) & (anomaly_df["News_Sentiment"] < -0.5)).astype(int)

print(anomaly_df[["Date", "Close", "Price_Change", "Anomaly_IF", "Anomaly_AE", "High_Negative_Impact"]])

