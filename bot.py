import tweepy
import requests
import os
import sys

# Get keys from the Brain repo's own secrets
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# This will be passed from the "signal" sent by your other repo
REPO_TO_CHECK = os.getenv("TARGET_REPO") 

def get_latest_commit():
    url = f"https://api.github.com/repos/{REPO_TO_CHECK}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

def tweet_commit(commit_data):
    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    message = commit_data['commit']['message']
    url = commit_data['html_url']
    repo_name = REPO_TO_CHECK.split('/')[-1]
    
    tweet_text = f"🚀 New Commit to {repo_name}:\n\n'{message}'\n\n{url}"
    
    try:
        client.create_tweet(text=tweet_text)
        print(f"Tweeted for {REPO_TO_CHECK}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    commit = get_latest_commit()
    if commit:
        tweet_commit(commit)
