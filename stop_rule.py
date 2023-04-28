import os
import json
import logging
from pathlib import Path

# Set up the script directory
script_directory = "directory"

# Set up logging
log_path = os.path.join(script_directory, "torrent_rule.log")
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(message)s')

# Check if the rule exists and run or cancel the rule
rule_file_path = os.path.join(script_directory, "torrent_rule.json")
rule_file = Path(rule_file_path)

if rule_file.is_file():
    with open(rule_file_path, "r") as f:
        rule = json.load(f)
        if rule["running"]:
            rule["running"] = False
            print("Rule stopped.")
            logging.info("Rule stopped.")
        else:
            print("The rule is not running.")
            logging.info("The rule is not running.")
    with open(rule_file_path, "w") as f:
        json.dump(rule, f)
else:
    print("No rule found.")
    logging.error("No rule found.")
