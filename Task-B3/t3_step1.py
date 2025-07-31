import re
import csv
from datetime import datetime

# Paths
log_path = "auth.log"
output_csv = "ssh_connections.csv"

# Pattern to match successful SSH logins
success_pattern = re.compile(
    r'^(?P<timestamp>\w{3} +\d+ \d{2}:\d{2}:\d{2}) .*sshd.*Accepted \w+ for (?P<user>\w+) from (?P<ip>\d+\.\d+\.\d+\.\d+)'
)

entries = []

# Read log file
with open(log_path, "r") as file:
    for line in file:
        match = success_pattern.search(line)
        if match:
            raw_ts = match.group("timestamp")
            ip = match.group("ip")

            # Parse to full datetime string
            full_ts = datetime.strptime(f"2023 {raw_ts}", "%Y %b %d %H:%M:%S")  # Assuming year 2023
            entries.append([full_ts.strftime("%Y-%m-%d %H:%M:%S"), ip])

# Write to CSV
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "IP Address"])
    writer.writerows(entries)

print(f"✅ Extracted {len(entries)} successful SSH connections to {output_csv}")
