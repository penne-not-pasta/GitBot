import tweepy
import requests
import os

# --- Configuration using Environment Variables ---
# These names must match the "Secrets" you create in GitHub Settings
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# GITHUB_REPOSITORY is automatically provided by GitHub Actions (e.g., "username/repo")
REPO_FULL_NAME = os.getenv("GITHUB_REPOSITORY")
LAST_COMMIT_FILE = "last_commit.txt"

def get_latest_commit():
    if not REPO_FULL_NAME:
        print("Error: GITHUB_REPOSITORY env var not found.")
        return None
        
    url = f"https://api.github.com/repos/{REPO_FULL_NAME}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

def tweet_commit(commit_data):
    # Initialize Tweepy Client (v2 API)
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    message = commit_data['commit']['message']
    url = commit_data['html_url']
    repo_name = REPO_FULL_NAME.split('/')[-1]
    
    tweet_text = f"🚀 New Commit to {repo_name}:\n\n'{message}'\n\nCheck it out: {url}"
    
    try:
        client.create_tweet(text=tweet_text)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Failed to post tweet: {e}")

def main():
    commit = get_latest_commit()
    if not commit:
        return

    current_sha = commit['sha']

    # Read the last saved SHA to avoid duplicates
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as f:
            last_sha = f.read().strip()
    else:
        last_sha = ""

    if current_sha != last_sha:
        tweet_commit(commit)
        # Save the new SHA so we don't tweet it again next time
        with open(LAST_COMMIT_FILE, "w") as f:
            f.write(current_sha)
    else:
        print("No new commits found since last check.")

if __name__ == "__main__":
    main()