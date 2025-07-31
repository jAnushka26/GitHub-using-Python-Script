import argparse
import os
import requests
 
def create_repo(org, repo, token):
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "name": repo,
        "private": False  # Change to True if you want private repos
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Created repo: {org}/{repo}")
    elif response.status_code == 422:
        print(f"Repo already exists: {org}/{repo}")
    else:
        print(f"Failed to create {org}/{repo}: {response.status_code}, {response.text}")
 
def main():
    parser = argparse.ArgumentParser(description="Bulk create GitHub repos from a file.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path to text file with org_name/repo_name lines")
    parser.add_argument('-t', '--token_env', type=str, required=True, help="Name of env variable storing GitHub token")
    args = parser.parse_args()
 
    token = os.environ.get(args.token_env)
    if not token:
        print(f"Environment variable '{args.token_env}' not found.")
        return
 
    with open(args.file, 'r') as file:
        for line in file:
            org_repo = line.strip()
            if '/' in org_repo:
                org, repo = org_repo.split('/')
                create_repo(org.strip(), repo.strip(), token)
            else:
                print(f"Invalid format (should be org/repo): {org_repo}")
 
if __name__ == "__main__":
    main()
 