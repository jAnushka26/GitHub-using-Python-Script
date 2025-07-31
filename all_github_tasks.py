import requests
from config import GITHUB_USERNAME, GITHUB_TOKEN

    # Get the GitHub user ID for a given username using a personal access token (PAT).
def get_user_id(pat, username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception(f"Could not find user {username}: {response.status_code}")

    # Invite a user to a GitHub organization with a specified role (default: direct_member).
def invite_user_to_org(pat, org_name, username, role="direct_member"):
    url = f"https://api.github.com/orgs/{org_name}/invitations"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "invitee_id": get_user_id(pat, username),
        "role": role
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Invitation sent to {username}")
    else:
        print(f"Failed to invite {username}: {response.status_code} - {response.json()}")
    return response.json()

    # Create a new GitHub repository, either in a user account or an organization.
def create_github_repo(repo_name, description="", private=True, auto_init=True, org_name=None):
    if org_name:
        url = f"https://api.github.com/orgs/{org_name}/repos"
    else:
        url = "https://api.github.com/user/repos"
    headers = {
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": auto_init
    }
    response = requests.post(url, json=payload, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
        return response.json()
    else:
        print(f"Failed to create repository: {response.status_code} !!!")
        print("Error:", response.json())
        return None

    # Create a new team in a GitHub organization with an optional description and privacy setting.
def create_team(pat, org_name, team_name, description="", privacy="closed"):
    url = f"https://api.github.com/orgs/{org_name}/teams"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "name": team_name,
        "description": description,
        "privacy": privacy
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Team '{team_name}' created in organization '{org_name}'.")
        return response.json()
    elif response.status_code == 422 and 'already exists' in str(response.json()):
        print(f"Team '{team_name}' already exists in organization '{org_name}'.")
        return response.json()
    else:
        print(f"Failed to create team: {response.status_code} - {response.json()}")
        return None

    # Add a user to a team in a GitHub organization with a specified role (default: member).
def add_user_to_team(pat, org_name, team_slug, username, role="member"):
    url = f"https://api.github.com/orgs/{org_name}/teams/{team_slug}/memberships/{username}"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "role": role
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in (200, 201):
        print(f"User '{username}' added to team '{team_slug}'.")
        return response.json()
    else:
        print(f"Failed to add user to team: {response.status_code} - {response.json()}")
        return None

if __name__ == "__main__":
    pat = GITHUB_TOKEN
    org_name = "source-demo-org"
    github_username = "rani-ukamble"
    repo_name = "public-repo-created-via-script"
    description = "This repo was created using a Python script and GitHub API."
    team_name = "Team-Python-GitHub-NGT"

    # 1. Invite user to organization
    invite_user_to_org(pat, org_name, github_username)

    # 2. Create a repository in the organization
    create_github_repo(repo_name, description, private=False, org_name=org_name)

    # 3. Create a team in the organization
    create_team(pat, org_name, team_name, description="Demo team")

    # 4. Add user to the team
    team_slug = team_name.lower().replace(" ", "-")
    add_user_to_team(pat, org_name, team_slug, github_username)