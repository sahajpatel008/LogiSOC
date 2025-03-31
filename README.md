# LogiSOC
A web application for SOC analysts

### Table of Contents

- [Live Demo](#demo)
- [Logs Dataset](#logs-dataset)  
- [Anomaly Detection](#anomaly-detection)  
  - [Top domain referrers](#top-domain-referrers)  
  - [Top requested pages](#top-requested-pages)  
  - [Malicious Domains](#malicious-domains)  
  - [Traffic proportion](#traffic-proportion)  
  - [Detection of endpoint scanners via 404s](#detection-of-endpoint-scanners-via-404s)  
  - [Detection of Scraping or Brute force via 429s](#detection-of-scraping-or-brute-force-vis-429s)  
  - [Detection of Burst Activity](#detection-of-burst-activity)  
  - [Detection of Data Exfiltration Attempts](#detection-of-data-exfiltration-attempts)  
  - [Activity Timeline](#activity-timeline)  
- [Run with Docker](#run-with-docker)
- [Deploying locally](#deploying-locally)  
  - [Backend](#backend)  
  - [Frontend](#frontend)

## Demo
Live at:  https://logisoc-frontend.fly.dev/ 
For log files see [Logs Dataset](#logs-dataset) 

## Logs Dataset
I have used the [SecRepo](https://www.secrepo.com/)'s => [Web Server Access Logs](https://www.secrepo.com/self.logs/). Any of the web access logs can be used for analysis. Some of them are stored in `log_samples/`.

> ⚠️ **IMPORTANT:**  
> **BEFORE YOU DO ANALYSIS: PLEASE CHANGE THE EXTENSION OF THESE FILES TO `.log` IF NOT ALREADY.**  
> This step is required for the analysis to work correctly.
> `log_samples/` already has files with .log extension. 

## Anomaly Detection
1. ### Top domain referrers
    - This function processes the referrer column in the data to find which external websites most frequently directed users to the site. It filters for valid HTTP URLs, extracts just the domain part, counts how often each domain appears, and returns the top N most common ones. 
    - Unusual or sudden changes in top referrer domains can indicate suspicious activity, like bots or malicious redirections.
2. ### Top requested pages  
    - This function finds the most frequently accessed pages on the site by counting how often each request_path appears in the data. It returns the top N pages based on request count.
    - A sudden spike in requests to uncommon or sensitive pages may signal probing, attacks, or unauthorized access attempts
3. ### Malicious Domains
    - Check the domains of top referrers from 1. 
    - Queries the VirusTotal API to check if a given domain has been flagged as malicious, suspicious, or safe. It returns a summary of the latest analysis statistics for that domain.

4. ### Traffic proportion
    - Classifies HTTP response codes into categories like Allowed, Blocked, Server Error, or Other, then summarizes the count of each type to give an overview of traffic behavior.
    - A sudden rise in Blocked or Server Error responses can indicate access attempts to restricted resources, misconfigurations, or potential attacks like brute-force or DDoS.

5. ### Detection of endpoint scanners via 404s
    - Identifies IP addresses that triggered a high number of 404 (Not Found) errors, which often indicates scanning for non-existent or sensitive endpoints.
    -  Multiple 404 responses from the same IP may signal reconnaissance or probing activity, potentially preceding an attack.

6. ### Detection of Scraping or Brute force vis 429s
    - Flags IP addresses that receive too many 429 (Too Many Requests) errors, which often indicates automated activity like scraping or brute-force attacks.
    - Frequent 429 responses from the same IP suggest abnormal request patterns, helping identify bots or attackers overloading the server.
7. ### Detection of Burst Activity
    - Detects IPs that trigger multiple identical response codes (like 404 or 429) within a short time window, indicating sudden spikes in activity.
    -  Rapid bursts of errors from the same IP may suggest automated scanning, scraping, or attack attempts in a short span of time.
8. ### Detection of Data Exfiltration Attempts
    -  Analyze logs to flag IPs making unusually large POST/PUT requests to unknown domains — a common sign of potential data exfiltration. It reads the logs, filters suspicious entries, and returns the findings in a structured format. 
    -  Large outbound data transfers to unfamiliar domains may indicate unauthorized data leakage or compromised systems attempting to exfiltrate sensitive information.
9. ### Activity Timeline
    - This function creates a 2-hour interval timeline of request volume by grouping log timestamps. It helps visualize traffic trends over time.
    - Sudden spikes or drops in activity can reveal unusual behavior, such as bursts of automated traffic, downtime, or potential attacks.

## Run with Docker
---
This app consists of a React (Vite) frontend and a Flask backend, orchestrated with Docker Compose.
1. Open cmd, be at the root level
2. You need to pass the VITE_CLERK_PUBLISHABLE_KEY environment variable when building the containers.
    For Linux/Mac:
    ```sh
    VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key_here docker-compose up --build
    ```
    For Windows (Command Prompt):
    ```sh
    set VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key_here
    ```
    ```sh
    docker-compose up --build
    ```
    VITE_BASE_URL is hardcoded as http://localhost:5000 in the docker-compose.yml.
    Replace your_clerk_key_here with your actual Clerk publishable key.

## Deploying locally
---

### Backend
1. Clone the repository and navigate to the backend folder:
    ```sh
        git clone https://github.com/sahajpatel008/LogiSOC.git
    ```
2. Navigate to the frontend folder
    ```sh
    cd LogiSOC
    ```
3. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install dependencies:
    ```sh
    pip install -r backend/requirements.txt
    ```
5. Make backend/.env file
    ```sh
    VIRUS_TOTAL_KEY=#enter your virus  total key
    CLERK_JWT_ISSUER= #enter from clerk API website, (project settings -> api )
    CLERK_JWKS_URL= #enter from clerk API website
    CLERK_AUDIENCE= #enter from clerk API website
    ```
6. Navigate to the backend folder
    ```sh
    cd backend
    ```
7. Running the flask server
    ```sh
    python app.py
    ```
The backend server will start on http://localhost:5000 by default.

---

### Frontend
1. Navigate to the frontend folder
    ```sh
    cd frontend
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Set up the .env file in the  frontend/ level. (root level of react project)
    ```sh
    VITE_CLERK_PUBLISHABLE_KEY=#your public clerk frontend key
    VITE_BASE_URL=#where your frontend is running, eg: http://127.0.0.1:5000
    ```
4. Running the development server
    ```sh
    npm run dev
    ```
