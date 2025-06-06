import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Twitter API v2 client authentication (OAuth 1.0a User Context)
def twitter_client():
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
        wait_on_rate_limit=True
    )
    return client

# Google Sheets authentication
def get_gsheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds/service_account.json', scope)
    client = gspread.authorize(creds)
    return client.open(os.getenv("GOOGLE_SHEET_NAME")).sheet1

# Generate tweet content
def generate_tweet():
    return f"Hello world! 🌍 This tweet was auto-posted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

# Validate tweet content length
def is_valid_tweet(tweet):
    return 0 < len(tweet) <= 280

# Log to Google Sheet
def log_to_sheet(status, content, details=""):
    sheet = get_gsheet()
    sheet.append_row([datetime.now().isoformat(), status, content, details])

# Main function
def main():
    tweet = generate_tweet()

    if not is_valid_tweet(tweet):
        print("❌ Invalid tweet content")
        log_to_sheet("Validation Error", tweet, "Tweet exceeds 280 chars or is empty")
        return

    try:
        client = twitter_client()
        # Post tweet with Twitter API v2
        response = client.create_tweet(text=tweet)
        print("✅ Tweet posted successfully!")
        log_to_sheet("Success", tweet, f"Tweet ID: {response.data['id']}")
    except Exception as e:
        print("❌ Twitter error:", e)
        log_to_sheet("Twitter Error", tweet, str(e))

if __name__ == "__main__":
    main()
