import pandas as pd
import re
from pathlib import Path
from datetime import datetime

def convert_to_df(filepath):
    # Load the log file
    with open(filepath, "r") as file:
        logs = file.readlines()

    # Regex pattern for log parsing
    pattern = r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<request_path>\S+) (?P<http_version>[^"]+)" (?P<status_code>\d+) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'

    # Parse each log line
    parsed_logs = [re.match(pattern, line).groupdict() for line in logs if re.match(pattern, line)]

    # Convert to DataFrame
    df = pd.DataFrame(parsed_logs)

    # Optional: convert timestamp to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')

    # Dynamically get path to resources folder
    resources_path = Path(__file__).resolve().parent / "resources"
    resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

    output_csv_path = resources_path / "LOGS.csv"
    df.to_csv(output_csv_path, index=False)

    print(f"Saved parsed logs to {output_csv_path}")
    print(df.head())