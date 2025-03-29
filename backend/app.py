import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from logic import convert_to_df, get_top_referer_domains, get_top_requested_pages, \
    check_domains, get_blocked_vs_allowed_traffic, detect_endpoint_scanning_by_404, \
    detect_scraping_by_429, detect_burst_activity
from dotenv import load_dotenv
import pandas as pd
import traceback
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
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = get_top_referer_domains(df)
        # Dynamically get path to resources folder
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "2_topDomainReferers.csv"
        result_df.to_csv(output_csv_path, index=False)
        result = result_df.to_dict(orient="records")
        
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@app.route('/top-page-visits', methods=['GET'])
def top_page_visits():
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "LOGS.csv"
        df = pd.read_csv(csv_path)

        # Get top referer domains
        result_df = get_top_requested_pages(df)
        result = result_df.to_dict(orient="records")

        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@app.route('/check-domains', methods=['POST'])
def malicious_domain_check():
    try:
        # Read DataFrame from resources/LOGS.csv
        csv_path = Path(__file__).resolve().parent / "resources" / "2_topDomainReferers.csv"
        df = pd.read_csv(csv_path)
        
        results = check_domains(list(df['Domains']), str(VIRUS_TOTAL_KEY), 2)
        resources_path = Path(__file__).resolve().parent / "resources"
        resources_path.mkdir(exist_ok=True)  # create resources/ if it doesn't exist

        output_csv_path = resources_path / "3_maliciousDomainsCheck.csv"
        results.to_csv(output_csv_path, index=False)
        
        return jsonify(results.to_dict(orient="records")), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/request-status', methods=['GET'])
def get_status_codes_pie_chart():
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
        result = result_df.to_dict(orient="records")
        
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@app.route('/404-error-ips', methods=['GET'])
def get_404_error_IPs():
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
        result = result_df.to_dict(orient="records")
        
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/429-error-ips', methods=['GET'])
def get_429_error_IPs():
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
        result = result_df.to_dict(orient="records")
        
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@app.route('/burstActivity', methods=['GET'])
def get_burstActivity():
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
        result = result_df.to_dict(orient="records")
        
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
