import os
import hashlib
import json
import requests

GITHUB_USER = "ALW-N" 
ZIP_DIR = "zips"
UPLOAD_DIR = "upload"
CHECKSUM_FILE = "checksums.json"

os.makedirs(ZIP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load or initialize checksums
if os.path.exists(CHECKSUM_FILE):
    with open(CHECKSUM_FILE, "r") as f:
        checksums = json.load(f)
else:
    checksums = {}

def sha256_checksum(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# Get all repos
print("🔍 Fetching repositories...")
repos_response = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos")

if repos_response.status_code != 200:
    print("❌ Failed to fetch repositories. Status:", repos_response.status_code)
    print("Response:", repos_response.text)
    exit(1)

repos = repos_response.json()


for repo in repos:
    repo_name = repo["name"]

    # Get all branches for the repo
    branches_response = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/branches")
    branches = branches_response.json()

    for branch in branches:
        branch_name = branch["name"]
        zip_url = f"https://github.com/{GITHUB_USER}/{repo_name}/archive/refs/heads/{branch_name}.zip"
        zip_filename = f"{repo_name}-{branch_name}.zip"
        zip_path = os.path.join(ZIP_DIR, zip_filename)
        temp_path = os.path.join(ZIP_DIR, "temp.zip")

        # Download the zip to a temp file
        r = requests.get(zip_url)
        with open(temp_path, "wb") as f:
            f.write(r.content)

        # Compute new checksum
        new_checksum = sha256_checksum(temp_path)
        key = f"{repo_name}-{branch_name}"

        if checksums.get(key) != new_checksum:
            # New or updated zip
            if os.path.exists(zip_path):
                os.remove(zip_path)
            os.rename(temp_path, zip_path)

            # Update checksum
            checksums[key] = new_checksum

            # Copy to upload directory
            upload_path = os.path.join(UPLOAD_DIR, zip_filename)
            with open(zip_path, "rb") as src, open(upload_path, "wb") as dst:
                dst.write(src.read())

            print(f"⬇️  Downloaded/Updated: {zip_filename}")
        else:
            # No change
            os.remove(temp_path)
            print(f"⚠️  No change in: {zip_filename} (skipping)")

# Save updated checksums
with open(CHECKSUM_FILE, "w") as f:
    json.dump(checksums, f, indent=2)

print("✅ Done.")
