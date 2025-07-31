import requests
import datetime
import sys
import time
import csv


REPO = "tensorflow/tensorflow"
START_DATE = datetime.datetime(2023, 1, 1)
CSV_FILE = "weekly_loc_stats.csv"

def fetch_contributor_stats(repo):
    url = f"https://api.github.com/repos/{repo}/stats/contributors"
    print(f"📡 Fetching contributor stats for {repo}...")

    for attempt in range(10):  # Retry up to 10 times if data is being generated
        response = requests.get(url)
        if response.status_code == 202:
            print("⏳ GitHub is generating stats. Retrying in 3s...")
            time.sleep(3)
            continue
        elif response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch data: {response.status_code}")
            sys.exit(1)
    print("❌ GitHub stats still not ready. Try again later.")
    sys.exit(1)

def save_to_csv(stats, filename):
    print(f"💾 Saving data to {filename}...")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Contributor", "Week Start", "Lines Added", "Lines Deleted", "Commits"])

        for contributor in stats:
            user = contributor.get("author", {}).get("login", "unknown")
            for week in contributor.get("weeks", []):
                week_start = datetime.datetime.fromtimestamp(week["w"])
                if week_start >= START_DATE:
                    added = week["a"]
                    deleted = week["d"]
                    commits = week["c"]
                    if added or deleted or commits:
                        writer.writerow([user, week_start.date(), added, deleted, commits])
    print("✅ CSV export complete.")

def display_weekly_loc(stats):
    print(f"\n📊 Weekly LOC data since {START_DATE.date()}:\n")
    for contributor in stats:
        user = contributor.get("author", {}).get("login", "unknown")
        print(f"👤 {user}")
        for week in contributor.get("weeks", []):
            week_start = datetime.datetime.fromtimestamp(week["w"])
            if week_start >= START_DATE:
                added = week["a"]
                deleted = week["d"]
                commits = week["c"]
                if added or deleted or commits:
                    print(f"  📅 {week_start.date()} → +{added} / -{deleted} ({commits} commits)")
        print("-" * 40)

if __name__ == "__main__":
    stats = fetch_contributor_stats(REPO)
    display_weekly_loc(stats)
    save_to_csv(stats, CSV_FILE)
