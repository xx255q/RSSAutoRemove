import os
import sys
import time
import json
import logging
import schedule
import qbittorrentapi
from pathlib import Path

# Configuration
ip_address = 'IP'
webui_port = 8999
webui_username = 'Username'
webui_password = 'Password'
rss_feed_url = 'RSS URL'

# Set up the script directory
script_directory = "Whatever directory"

# Set up logging
log_path = os.path.join(script_directory, "torrent_rule.log")
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(message)s')

# Connect to qBittorrent
try:
    qbt_client = qbittorrentapi.Client(host=f'http://{ip_address}:{webui_port}/', username=webui_username, password=webui_password)
    qbt_client.auth_log_in()
    print("Connected to qBittorrent.")
    logging.info("Connected to qBittorrent.")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__} - {str(e)}")
    logging.error("Unexpected error: %s - %s", type(e).__name__, e)
    sys.exit(1)

# Function to remove torrents older than 1 day
def remove_old_torrents():
    torrents = qbt_client.torrents_info(status_filter='completed')
    for torrent in torrents:
        if torrent.completion_on + 86400 < time.time():
            qbt_client.torrents_delete(torrent_hashes=torrent.hash)
            logging.info(f"Removed torrent: {torrent.name}")

# Schedule job
schedule.every(1).days.at("00:00").do(remove_old_torrents)

# Check if the rule exists and run or cancel the rule
rule_file_path = os.path.join(script_directory, "torrent_rule.json")
rule_file = Path(rule_file_path)

if rule_file.is_file():
    with open(rule_file_path, "r") as f:
        rule = json.load(f)
        if rule["running"]:
            choice = input("The rule is already running. Would you like to cancel it? (Y/N): ")
            if choice.lower() == "y":
                rule["running"] = False
                schedule.clear()
                print("Rule canceled.")
                logging.info("Rule canceled.")
        else:
            rule["running"] = True
            print("Rule is now running.")
            logging.info("Rule is now running.")
else:
    rule = {"running": True}
    print("Rule created and is now running.")
    logging.info("Rule created and is now running.")

# Save rule status
with open(rule_file_path, "w") as f:
    json.dump(rule, f)

# Run the scheduled tasks
while rule["running"]:
    schedule.run_pending()
    time.sleep(60)
