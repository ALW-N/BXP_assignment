import re
import csv
from datetime import datetime

# Input and output files
log_path = "auth.log"
output_csv = "vagrant_ssh_activity.csv"

entries = []

# Regex for all success logins (vagrant only, port optional)
success_pattern = re.compile(
    r'^(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*Accepted \w+ for (?P<user>vagrant) from (?P<ip>\d+\.\d+\.\d+\.\d+)(?: port (?P<port>\d+))?'
)

# Regex for key mismatch failures (vagrant only, port optional)
failure_pattern = re.compile(
    r'^(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*Connection closed by (authenticating user )?(?P<user>vagrant)? ?(?P<ip>\d+\.\d+\.\d+\.\d+)(?: port (?P<port>\d+))?'
)

# Read log file
with open(log_path, "r") as file:
    for line in file:
        # Match success logins
        match = success_pattern.search(line)
        if match:
            ts = match.group("timestamp")
            dt = datetime.strptime(f"2023 {ts}", "%Y %b %d %H:%M:%S")  # assuming year
            entries.append([
                dt.strftime("%Y-%m-%d %H:%M:%S"),
                "vagrant",
                match.group("ip"),
                match.group("port") if match.group("port") else "N/A",
                "Success"
            ])
            continue

        # Match key mismatch failures
        match = failure_pattern.search(line)
        if match:
            ts = match.group("timestamp")
            dt = datetime.strptime(f"2023 {ts}", "%Y %b %d %H:%M:%S")
            entries.append([
                dt.strftime("%Y-%m-%d %H:%M:%S"),
                "vagrant",
                match.group("ip"),
                match.group("port") if match.group("port") else "N/A",
                "Key Mismatch"
            ])

# Write to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Username", "IP Address", "Port", "Status"])
    writer.writerows(entries)

print(f"✅ Extracted {len(entries)} vagrant login attempts saved to {output_csv}")
