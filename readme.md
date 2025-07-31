# DevOps Tasks


## 📦 How to Use This Repository

You can either:

### 🔽 Option 1: Download ZIP

1. Click on the green **`Code`** button in GitHub.
2. Select **`Download ZIP`**.
3. Extract the contents and open the folder in your IDE or terminal.

### 🔁 Option 2: Clone via Git

```bash
git clone https://github.com/ALW-N/BXP_assignment.git

cd BXP_assignment
```

## Prerequisites

- Python 3.6 or above should be installed.
- Internet connection is required to fetch GitHub data.
- Required Python packages:
  ```bash
  pip install requests
---

# Task #B1

---

### 1. Write a Bash/Python Script to download a Zip file for all the branches of all the repositories in a github URL (your github URL).

#### 📂 File Location
```bash
cd Task-B1

python t1_step1.py
```
💬 **Description**  

- Fetches all repositories from my GitHub username (ALW-N)
- For each repository, fetches all branches
- Downloads a .zip archive for each branch into the zips/ folder

### 2. Modify the Bash/Python Script to upload the downloaded zips made in Step 1.


```bash
python t1_step2.py
```
💬 **Description**  

- Takes all the .zip files downloaded in zips/ folder (created from Step 1)
- Copies them to an upload/ folder
- This simulates preparing files for upload or further use
- Ensures all downloaded zips are stored in a separate upload-ready directory


### 3. Modify the Bash/Python Script to download only those zips (combination of repository-branch) only if there is a change in Checksum of the zip. Assume that steps 1,2 and 3 will be run daily.
```bash
python t1_step3.py
```

💬 **Description**  

- Checks all GitHub repositories and branches for the user ALW-N
- Downloads each branch .zip temporarily
- Calculates a checksum (SHA256) and compares it with the stored version in checksums.json
- Only if there's a change:
    - The old zip is replaced with the updated one in zips/
    -  It is also copied to the upload/ folder
    -  The checksum is updated

- If no change is found, it skips the download
- This ensures efficient daily syncing without duplicate downloads

# Task #B2

### 1. Write a Bash/Python Script to generate the code contribution of any public GitHub repository (as input) and print the lines of code (LOC) added/removed/updated per week by individual contributors from 01-Jan-2023 till Current Date.

💬 **Description**  
- This script collects weekly contribution data (lines added, deleted, commits) from a given public GitHub repository starting from **01-Jan-2023** to the current date.

---

#### 📂 File Location
```bash
cd ../Task-B2
python t2.py
```
🔐 Note: This script uses the public repository tensorflow/tensorflow as the input GitHub repository.

# Task #B3

### 1. Write a Bash/Python Script to pick up Syslog of a linux system (/var/log/auth.log) and read the File to check ssh connections into the Machine. Output the IP Address and Time of SSH into a CSV File.

#### 📂 File Location
```bash
cd ../task-b3
python t3_step1.py
```

💬 **Description**  
- This script parses a Linux auth.log file to extract successful SSH login attempts, including the timestamp and IP address. The result is saved into a CSV file.

    - File: t3_step1.py

    - Sample Input: auth.log file (placed in task-b3/)

    - Output: ssh_connections.csv

### 2. Modify the script to also add all instances into the CSV file when the login was rejected due to Key Mismatch.
```bash
python t3_step2.py
```

💬 **Description** 

This updated script captures both:

- ✅ Successful logins (via public key)

- ❌ Failed logins (due to key mismatch)

🔐Note: Only vagrant user's attempts are included, as per the assignment scope.

<br>

## 🛑  Limitations

This project uses unauthenticated GitHub API requests. As a result, it is subject to GitHub's lower rate limits (typically 60 requests per hour per IP address). If you encounter errors like 403: rate limit exceeded, please wait for an hour before you continue