# LogiSOC
A web application for SOC analysts


## Deploying locally
---

### Backend
1. Clone the repository and navigate to the backend folder:
    ```sh
        https://github.com/sahajpatel008/LogiSOC.git
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Make .env file on the root level (same level .gitignore)
    ```sh
    VIRUS_TOTAL_KEY=#enter your virus  total key
    ```
5. Running the flask server
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
