import json
import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from logic import convert_to_df, get_top_referer_domains, get_top_requested_pages, \
    check_domains, get_blocked_vs_allowed_traffic, detect_endpoint_scanning_by_404, \
    detect_scraping_by_429, detect_burst_activity,  detect_data_exfiltration
from dotenv import load_dotenv
import pandas as pd
import traceback
from auth import verify_clerk_token
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

load_dotenv()
VIRUS_TOTAL_KEY = os.getenv("VIRUS_TOTAL_KEY")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, Flask is working!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    verify_clerk_token()
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_path)
        convert_to_df(saved_path)
        return jsonify({"message": f"File '{filename}' processed and uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/top-referers', methods=['GET'])
def top_referers():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = get_top_referer_domains(df)

        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        # Save result to CSV
        output_csv_path = resources_path / "2_topDomainReferers.csv"
        result_df.to_csv(output_csv_path, index=False)

        # Convert result to dict with columns and rows
        result = {
            "title": "Top Referer domains",
            "infoText": "Displays the most common external domains that directed users to your website. This can help identify unexpected traffic sources, detect potential phishing campaigns, malicious redirections, or referral-based attacks. Analysts can use this to spot anomalies or validate the legitimacy of inbound traffic.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }

        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    
@app.route('/top-page-visits', methods=['GET'])
def top_page_visits():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = get_top_requested_pages(df)

        # Convert to dict with columns and rows
        result = {
            "title": "Top page visits",
            "infoText": "Shows the most requested internal pages. Helps detect unusual activity, high-interest endpoints, or potential scanning behavior.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }

        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    
@app.route('/check-domains', methods=['GET'])
def malicious_domain_check():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "2_topDomainReferers.csv"
        df = pd.read_csv(csv_path)
        
        results = check_domains(list(df['Domains']), str(VIRUS_TOTAL_KEY), 2)
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "3_maliciousDomainsCheck.csv"
        results = results.fillna("N/A")
        results.to_csv(output_csv_path, index=False)
        
        result = {
            "title": "Malicious domains Check",
            "infoText": " VirusTotal scan summary to flag suspicious or malicious referrers.",
            "columns": list(results.columns),
            "rows": results.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/request-status', methods=['GET'])
def get_status_codes_pie_chart():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get numbers
        result_df = get_blocked_vs_allowed_traffic(df)
        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "4_blocked_unblocked_analysis.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = {
            "title": "Traffic requests distribution",
            "infoText": " Categorizes requests as Allowed, Blocked, or Server Errors based on response codes. Helps identify access issues or abnormal traffic patterns.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@app.route('/404-error-ips', methods=['GET'])
def get_404_error_IPs():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = detect_endpoint_scanning_by_404(df)
        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "5_endpointScanningDomains.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = {
            "title": "Frequent 404 Error IPs",
            "infoText": "Flags IPs with excessive 404 errors, which may indicate scanning for non-existent or restricted endpoints.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    

@app.route('/429-error-ips', methods=['GET'])
def get_429_error_IPs():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = detect_scraping_by_429(df)
        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "5_flaggedScrappingDomains.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = {
            "title": "Frequent 429 error IPs",
            "infoText": " Identifies IPs repeatedly hitting rate limits — possible scraping or brute-force.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
    
@app.route('/burstActivity', methods=['GET'])
def get_burstActivity():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        burst_404_df = detect_burst_activity(df, 404, 5)
        burst_429_df = detect_burst_activity(df, 429, 5)

        result_df = pd.concat([burst_404_df, burst_429_df], ignore_index=True)

        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "6_burst_activity.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = {
            "title": "Burst Activity",
            "infoText": "Flags IPs with rapid 404/429 responses in a short time, suggesting scanning, scraping, or brute-force behavior.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
    
@app.route('/get-data-exfiltration', methods=['GET'])
def get_exfiltration_attempts():
    verify_clerk_token()
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = detect_data_exfiltration(df, 10000)
        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "7_dataExfiltrationIPs.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = {
            "title":"Suspected data exfiltration attempts",
            "infoText": " Flags large POST/PUT requests to unknown domains, which may indicate unauthorized data transfers.",
            "columns": list(result_df.columns),
            "rows": result_df.values.tolist()
        }
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
def getPath(fileName):
    return Path(__file__).resolve().parent / "resources" / str(fileName)

@app.route('/activity-timeline')
def activity_timeline():
    verify_clerk_token()
    try:
        df = pd.read_csv(getPath('LOGS.csv'))
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Group by hour
        timeline = df.set_index('timestamp').resample('2H').size()

        # Convert to JSON-friendly format
        timeline_data = [
            {"time": time.strftime("%H:00"), "count": int(count)}
            for time, count in timeline.items()
        ]

        return jsonify({
            "title": "Activity Timeline",
            "infoText": "Shows the volume of requests grouped by 2-hour intervals to help identify activity spikes or quiet periods.",
            "data": timeline_data
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/get-summary', methods=['GET'])
def get_summary():
    try:
        soc_learnings = []

        high_traffic_df = pd.read_csv(getPath('7_dataExfiltrationIPs.csv'))

        for ip in high_traffic_df[(high_traffic_df['method'] == 'POST') & (high_traffic_df['size'] > 1_000_000)]['ip'].unique():
            soc_learnings.append(f"High POST traffic detected from IP {ip}")
        
         # 404 scanning
        suspicious_404_ips = pd.read_csv(getPath("5_endpointScanningDomains.csv"))
        for ip in suspicious_404_ips['IP']:
            soc_learnings.append(f"Multiple failed access attempts from {ip}")

        suspicious_429_ips = pd.read_csv(getPath("5_flaggedScrappingDomains.csv"))
        for ip in suspicious_429_ips['IP']:
            soc_learnings.append(f"Too many requests (429) from {ip}")
        # Suspicious file downloads

        df = pd.read_csv(getPath('LOGS.csv'))
        suspicious_files = df[df['request_path'].str.contains(r'\.exe', case=False, na=False)]
        for _, row in suspicious_files.iterrows():
            dt = pd.to_datetime(row['timestamp']).strftime('%b %d')
            soc_learnings.append(f"Suspicious file download: {row['request_path']} on {dt}")

        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_json_path = resources_path / "8_soc_learnings.json"
        with open(output_json_path, "w") as f:
            json.dump(soc_learnings, f, indent=4)
        
        return jsonify(soc_learnings), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
