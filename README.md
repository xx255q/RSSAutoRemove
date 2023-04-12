# RSSAutoRemove

BitTorrent Auto-Remove Script
This script is designed to automatically remove torrent downloads from a specific RSS feed in qBittorrent after a set amount of time (1 day by default).

Features

Connects to qBittorrent WebUI using user-specified connection details (IP address, port, username, and password).

Monitors torrents downloaded from a specific RSS feed.

Automatically removes the torrents (without deleting files) after a specified time period (1 day by default).

Generates a log file with information about removed torrents.

Provides a user prompt to cancel the rule if the script is already running.

Prerequisites

Python 3.6 or higher installed on your system.
qBittorrent installed and configured with WebUI access.

Installation

Download the script file auto_remove_qbittorrent.py to your local machine.

Open the script file with a text editor and update the following variables with your qBittorrent WebUI connection details and RSS feed URL:

IP_ADDRESS

PORT

USERNAME

PASSWORD

RSS_FEED_URL

Usage

Open a command prompt or terminal window.

Navigate to the directory containing the auto_remove_qbittorrent.py script.

Run the script using the following command: python auto_remove_qbittorrent.py

The script will check the connection to qBittorrent WebUI and display a confirmation message if successful.

The script will continue running in the background, monitoring torrents from the specified RSS feed.

When a torrent reaches the specified time limit, it will be removed from qBittorrent and a log entry will be created in a file named removed_torrents.log in the same directory as the script.

If you run the script again while it's already running, you will receive a prompt asking if you want to cancel the existing rule.

Notes

The script is designed for qBittorrent and may not work with other torrent clients.

The script removes torrents without deleting the files. If you want to delete the files as well, you will need to modify the script accordingly.

The time period for torrent removal is set to 1 day by default, but it can be adjusted by modifying the TIME_TO_REMOVE variable in the script.

Ensure that your qBittorrent WebUI access details are correct and secure, as the script uses these to connect to your qBittorrent instance.
