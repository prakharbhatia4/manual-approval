import os
import time
import requests

GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']
ISSUE_NUMBER = os.environ['INPUT_ISSUE_NUMBER']
APPROVAL_COMMAND = os.environ.get('INPUT_APPROVAL_COMMAND', '/approve')
REPO = os.environ['GITHUB_REPOSITORY']

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_comments():
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

print(f"Waiting for approval command '{APPROVAL_COMMAND}' on issue/PR #{ISSUE_NUMBER}...")

while True:
    comments = get_comments()
    if any(comment['body'].strip() == APPROVAL_COMMAND for comment in comments):
        print("Approval received!")
        break
    print("No approval yet, sleeping for 60 seconds...")
    time.sleep(60)
