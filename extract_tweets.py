import requests
import pandas as pd
url = "https://twitter-api45.p.rapidapi.com/search.php"

querystring = {"query":"stock market OR investment OR finance","search_type":"Top"}

headers = {
	"x-rapidapi-key": "key",
	"x-rapidapi-host": "twitter-api45.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()  # Get JSON response

# 🔍 Extract relevant tweet data
tweets = []

try:
    for tweet in data.get("timeline", []):  # Loop through 'timeline' key
        tweets.append({
            "Tweet ID": tweet.get("tweet_id", "N/A"),
            "Username": tweet.get("screen_name", "N/A"),
            "Text": tweet.get("text", "N/A"),
            "Created At": tweet.get("created_at", "N/A"),
            "Likes": tweet.get("favorites", 0),
            "Replies": tweet.get("replies", 0),
            "Retweets": tweet.get("retweets", 0),
            "Views": tweet.get("views", "N/A"),
            "Bookmarks": tweet.get("bookmarks", 0),
            "User Followers": tweet.get("user_info", {}).get("followers_count", 0),
            "User Location": tweet.get("user_info", {}).get("location", "N/A")
        })

    # Convert extracted tweets to DataFrame and save as CSV
    df = pd.DataFrame(tweets)
    df.to_csv("twitter_finance_data.csv", index=False)

    print("✅ Saved extracted tweets to: twitter_finance_data.csv")

except KeyError as e:
    print(f"⚠️ KeyError: {e} - JSON structure might have changed!")