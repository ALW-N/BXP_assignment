import os
import requests
import shutil

# === CONFIGURATION ===
GITHUB_USER = "ALW-N"  # Replace with your GitHub username
ZIP_DIR = "zips"
UPLOAD_DIR = "upload"

# Create folders if they don't exist
os.makedirs(ZIP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Step 1: Get all repositories of the user
print("🔍 Fetching repositories...")
repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos"
repos_response = requests.get(repos_url)
repos = repos_response.json()

for repo in repos:
    repo_name = repo["name"]

    # Step 1.1: Get all branches of the repo
    branches_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/branches"
    branches_response = requests.get(branches_url)
    branches = branches_response.json()

    for branch in branches:
        branch_name = branch["name"]
        zip_url = f"https://github.com/{GITHUB_USER}/{repo_name}/archive/refs/heads/{branch_name}.zip"
        zip_filename = f"{repo_name}-{branch_name}.zip"
        zip_path = os.path.join(ZIP_DIR, zip_filename)

        # Step 1.2: Download the zip file
        response = requests.get(zip_url)
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print(f"⬇️  Downloaded: {zip_filename}")
        else:
            print(f"❌ Failed to download: {zip_filename}")

print("✅ All ZIP files downloaded successfully.")

# Step 2: Copy ZIPs to the upload/ folder
print("📦 Copying ZIPs to upload folder...")
for filename in os.listdir(ZIP_DIR):
    if filename.endswith(".zip"):
        src = os.path.join(ZIP_DIR, filename)
        dest = os.path.join(UPLOAD_DIR, filename)
        shutil.copy2(src, dest)
        print(f"✔️  Copied: {filename} → {UPLOAD_DIR}/")

print("✅ All files copied to upload folder.")
