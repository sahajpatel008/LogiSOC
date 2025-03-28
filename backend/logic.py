import pandas as pd
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

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

# Sample extract_domain helper
def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc or None
    except:
        return None

# Top accessed internal pages (based on request path)
def get_top_requested_pages(df, top_n=10):
    if 'request_path' not in df.columns:
        raise ValueError("Column 'request_path' not found in DataFrame")

    # Clean & count
    top_pages = df['request_path'].dropna().value_counts().head(top_n)
    return top_pages.reset_index().rename(columns={'index': 'Page', 'request_path': 'Pages'})

# Top external referer domains
def get_top_referer_domains(df, top_n=10):
    if 'referrer' not in df.columns:
        raise ValueError("Column 'referrer' not found in DataFrame")

    # Extract domain only from referer URLs that start with http
    referer_domains = df['referrer'].dropna()
    referer_domains = referer_domains[referer_domains.str.startswith('http', na=False)]
    referer_domains = referer_domains.apply(extract_domain).dropna()

    # Count frequency
    top_domains = referer_domains.value_counts().head(top_n)
    return top_domains.reset_index().rename(columns={'index': 'Domain', 'referrer': 'Domains'})
