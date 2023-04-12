import os
import sys
import time
import json
import logging
import schedule
import qbittorrentapi
from pathlib import Path

# Configuration
ip_address = 'ip address'
webui_port = 8999
webui_username = 'username'
webui_password = 'password'
rss_feed_url = 'URL'

# Set up logging
logging.basicConfig(filename='torrent_rule.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Connect to qBittorrent
try:
    qbt_client = qbittorrentapi.Client(host=f'http://{ip_address}:{webui_port}/', username=webui_username, password=webui_password)
    qbt_client.auth_log_in()
    print("Connected to qBittorrent.")
    logging.info("Connected to qBittorrent.")
except qbittorrentapi.LoginFailed as e:
    print("Connection to qBittorrent failed. Please check your credentials.")
    logging.error("Connection to qBittorrent failed: %s", e)
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
rule_file = Path("torrent_rule.json")
if rule_file.is_file():
    with open("torrent_rule.json", "r") as f:
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
with open("torrent_rule.json", "w") as f:
    json.dump(rule, f)

# Run the scheduled tasks
while rule["running"]:
    schedule.run_pending()
    time.sleep(60)
