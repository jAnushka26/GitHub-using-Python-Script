import os
import argparse
import requests
from config import SOURCE_PAT, REPO_LIST_FILE

def transfer_repository(source_pat, source_org, source_repo, target_org):
    url = f"https://api.github.com/repos/{source_org}/{source_repo}/transfer"
    headers = {
        "Authorization": f"token {source_pat}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "new_owner": target_org
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 202:
        print(f"Transfer initiated for: {source_org}/{source_repo} → {target_org}")
    else:
        print(f"Failed to transfer {source_repo}: {response.status_code} - {response.text}")

def migrate_repositories(source_pat, repo_list_file):
    # Read repos from the file
    try:
        with open(repo_list_file, "r") as f:
            lines = f.read().strip().splitlines()
    except FileNotFoundError:
        print(f"Repo list file not found: {repo_list_file}")
        return

    for line in lines:
        if "::" not in line:
            print(f"Invalid line skipped: {line}")
            continue

        try:
            source_full, target_full = line.strip().split("::")
            source_org, source_repo = source_full.strip().split("/")
            target_org, target_repo = target_full.strip().split("/")
        except ValueError:
            print(f"Malformed line skipped: {line}")
            continue

        print(f"\nTransferring {source_org}/{source_repo} → {target_org}/{target_repo}")
        transfer_repository(source_pat, source_org, source_repo, target_org)

def main():
    parser = argparse.ArgumentParser(description="Transfer GitHub repos from one org to another using GitHub API.")
    parser.add_argument("-f", "--repo-list-file", help="Path to repo list file", default=REPO_LIST_FILE)
    parser.add_argument("-s", "--source-pat", help="GitHub token for source org", default=SOURCE_PAT)
    args = parser.parse_args()

    # print(f"Using source PAT: {args.source_pat}")
    # print(f"Using repo list file: {args.repo_list_file}")


    migrate_repositories(
        source_pat=args.source_pat,
        repo_list_file=args.repo_list_file
    )

if __name__ == "__main__":
    main()
