import json
import pandas as pd
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import requests
import time

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

def check_domain_virustotal(domain, api_key):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        # You can return more info if needed
        return {
            'domain': domain,
            'harmless': stats.get('harmless', 0),
            'malicious': stats.get('malicious', 0),
            'suspicious': stats.get('suspicious', 0),
            'undetected': stats.get('undetected', 0),
        }
    else:
        return {
            'domain': domain,
            'harmless': '-',
            'malicious': '-',
            'suspicious': '-',
            'undetected': '-',
        }


def check_domains(domains, api_key, delay=15):
    results = []
    for domain in domains:
        result = check_domain_virustotal(domain, api_key)
        results.append(result)
        time.sleep(delay)  # VT API has rate limits for free users
    return pd.DataFrame(results)


def classify_traffic(code):
    try:
        code = int(code)
    except:
        return 'Other'
    
    if code in [200, 302]:
        return 'Allowed'
    elif code in [401, 403]:
        return 'Blocked'
    elif code in [500, 502, 503, 504]:
        return 'Server Error'
    else:
        return 'Other'

def get_blocked_vs_allowed_traffic(df):
    if 'status_code' not in df.columns:
        raise ValueError("DataFrame must have a 'response_code' column")

    df['traffic_status'] = df['status_code'].apply(classify_traffic)

    traffic_summary = df['traffic_status'].value_counts().reset_index()
    traffic_summary.columns = ['Status', 'Count']
    
    return traffic_summary


def detect_endpoint_scanning_by_404(df, threshold=10):
    if 'status_code' not in df.columns or 'ip' not in df.columns:
        raise ValueError("DataFrame must include 'status_code' and 'ip' columns")

    # Filter 404 entries
    df_404 = df[df['status_code'] == 404]

    # Count 404s per IP
    counts = df_404['ip'].value_counts()
    flagged_ips = counts[counts >= threshold].reset_index()
    flagged_ips.columns = ['IP', '404_Count']
    
    return flagged_ips

#possible scraping or brute force?
def detect_scraping_by_429(df, threshold=5):
    if 'status_code' not in df.columns or 'ip' not in df.columns:
        raise ValueError("DataFrame must include 'status_code' and 'ip' columns")

    # Filter 429 entries
    df_429 = df[df['status_code'] == 429]

    # Count 429s per IP
    counts = df_429['ip'].value_counts()
    flagged_ips = counts[counts >= threshold].reset_index()
    flagged_ips.columns = ['IP', '429_Count']
    
    return flagged_ips


def detect_burst_activity(df, response_code=404, threshold=5, window_minutes=1):
    if 'status_code' not in df.columns or 'ip' not in df.columns or 'timestamp' not in df.columns:
        raise ValueError("DataFrame must include 'status_code', 'ip', and 'timestamp' columns")

    # Ensure timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter for target response code (e.g., 404 or 429)
    df_filtered = df[df['status_code'] == response_code]

    # Sort by IP and timestamp
    df_filtered = df_filtered.sort_values(by=['ip', 'timestamp'])

    flagged_ips = set()

    # Group by IP and slide through timestamps
    for ip, group in df_filtered.groupby('ip'):
        times = group['timestamp'].tolist()
        for i in range(len(times) - threshold + 1):
            time_diff = (times[i + threshold - 1] - times[i]).total_seconds() / 60.0
            if time_diff <= window_minutes:
                flagged_ips.add(ip)
                break  # Once flagged, no need to keep checking that IP

    return pd.DataFrame({'IP': list(flagged_ips), 'Reason': [f'Burst {response_code} activity'] * len(flagged_ips)})


KNOWN_DOMAINS = [
    # "yourcompany.com",
    # "internal.service.net",
    # "api.yourapp.local"
]

def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return ""

def is_unknown_domain(domain, known_domains):
    return all(known not in domain for known in known_domains)

def detect_data_exfiltration(df, size_threshold=1_000_000, known_domains=KNOWN_DOMAINS):
    if 'size' not in df.columns or 'method' not in df.columns:
        raise ValueError("DataFrame must include 'response_size' and 'method' columns")
    
    # Optional: extract destination domain if available
    if 'request_path' in df.columns:
        df['destination_domain'] = df['request_path'].dropna().apply(extract_domain)
    elif 'referrer' in df.columns:
        df['destination_domain'] = df['referrer'].dropna().apply(extract_domain)
    else:
        df['destination_domain'] = ""

    # Filter by criteria
    df_suspect = df[
        (df['method'].str.upper().isin(['POST', 'PUT'])) &
        (df['size'] > size_threshold) &
        (df['destination_domain'].apply(lambda d: is_unknown_domain(d, known_domains)))
    ]
    
    return df_suspect[['ip', 'timestamp', 'method', 'request_path', 'size', 'destination_domain']]
