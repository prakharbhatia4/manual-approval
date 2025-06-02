import os
import time
import requests

GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']
ISSUE_NUMBER = os.environ['INPUT_ISSUE_NUMBER']
APPROVAL_COMMAND = os.environ.get('INPUT_APPROVAL_COMMAND', '/approve')
REPO = os.environ['GITHUB_REPOSITORY']
ALLOWED_APPROVERS = [user.strip() for user in os.environ.get('INPUT_APPROVERS', '').split(',') if user.strip()]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_comments():
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

print(f"Waiting for approval command '{APPROVAL_COMMAND}' on issue/PR #{ISSUE_NUMBER} from {ALLOWED_APPROVERS or 'anyone'}...")

while True:
    comments = get_comments()
    for comment in comments:
        if (comment['body'].strip() == APPROVAL_COMMAND and
            (not ALLOWED_APPROVERS or comment['user']['login'] in ALLOWED_APPROVERS)):
            print(f"Approval received from {comment['user']['login']}!")
            exit(0)
    print("No approval yet, sleeping for 60 seconds...")
    time.sleep(60)