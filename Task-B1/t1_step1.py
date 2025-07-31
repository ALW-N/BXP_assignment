import os
import requests

# === CONFIGURATION ===
GITHUB_USER = "ALW-N"  
ZIP_DIR = "zips"
os.makedirs(ZIP_DIR, exist_ok=True)

# Step 1: Get all repositories of the user
print("🔍 Fetching repositories...")
repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos"
repos_response = requests.get(repos_url)
repos = repos_response.json()

for repo in repos:
    repo_name = repo["name"]

    # Step 2: Get all branches of the repo
    branches_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/branches"
    branches_response = requests.get(branches_url)
    branches = branches_response.json()

    for branch in branches:
        branch_name = branch["name"]
        zip_url = f"https://github.com/{GITHUB_USER}/{repo_name}/archive/refs/heads/{branch_name}.zip"
        zip_filename = f"{repo_name}-{branch_name}.zip"
        zip_path = os.path.join(ZIP_DIR, zip_filename)

        # Step 3: Download the zip file
        response = requests.get(zip_url)
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print(f"⬇️  Downloaded: {zip_filename}")
        else:
            print(f"❌ Failed to download: {zip_filename}")

print("✅ All ZIP files downloaded successfully.")
