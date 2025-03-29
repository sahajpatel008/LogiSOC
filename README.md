# LogiSOC
A web application for SOC analysts


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
    pip install -r requirements.txt
    ```
5. Make .env file on the root level (same level .gitignore)
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
