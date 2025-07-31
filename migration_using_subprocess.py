import subprocess
import os
import argparse
import requests
from config import SOURCE_PAT, TARGET_PAT, WORK_DIR, REPO_LIST_FILE

def create_github_repo(org, repo, token, private=True):
   
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "name": repo,
        "private": private
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Created repo: {org}/{repo}")
        return True
    elif response.status_code == 422 and "already exists" in response.text:
        print(f"Repo already exists: {org}/{repo}")
        return True
    else:
        print(f"Failed to create repo {org}/{repo}: {response.text}")
        return False

def migrate_repositories(source_pat, target_pat, repo_list_file, work_dir):
    # Ensure working directory exists
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

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

        print(f"\nMigrating {source_org}/{source_repo} → {target_org}/{target_repo}")

        # Create target repo if it doesn't exist
        created = create_github_repo(target_org, target_repo, target_pat)
        if not created:
            print(f"Skipping migration for {source_org}/{source_repo}")
            continue

        source_url = f"https://{source_pat}@github.com/{source_org}/{source_repo}.git"
        target_url = f"https://{target_pat}@github.com/{target_org}/{target_repo}.git"
        local_path = os.path.join(work_dir, source_repo)

        # Clone source repo
        subprocess.run(["git", "clone", "--mirror", source_url, local_path])

        # Push to target repo
        subprocess.run(["git", "--git-dir", local_path, "push", "--mirror", target_url])

        print(f"Migration done for: {source_repo}")

def main():
    parser = argparse.ArgumentParser(description="Migrate GitHub repos from one org to another.")
    parser.add_argument("-f", "--repo-list-file", help="Path to repo list file")
    parser.add_argument("-d", "--work-dir", help="Working directory to clone repos")
    parser.add_argument("-s", "--source-pat", help="GitHub token for source org")
    parser.add_argument("-t", "--target-pat", help="GitHub token for target org")
    args = parser.parse_args()

    migrate_repositories(
        source_pat=args.source_pat,
        target_pat=args.target_pat,
        repo_list_file=args.repo_list_file,
        work_dir=args.work_dir
    )

if __name__ == "__main__":
    main()
