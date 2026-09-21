# CrediSphere AI

CrediSphere AI is a full-stack MCA project for intelligent credit risk assessment, loan processing, and fraud detection using multiple simulated AI/ML models.

## Technology Stack

*   **Frontend**: Vanilla HTML5, CSS3, JavaScript (No React/Angular/Tailwind)
*   **Backend**: Python Flask, Flask-SQLAlchemy, PostgreSQL
*   **Security**: JWT Authentication, Bcrypt Hashing, CORS
*   **AI/ML**: Mock implementations for Isolation Forest, XGBoost, LightGBM, EasyOCR/YOLOv8, GNN, Prophet, Random Forest, Bayesian Optimization, and Apriori.

## Setup Instructions (macOS)

### 1. Database & Environment Setup

The backend uses **SQLite** by default for easy local testing.

1. Open a terminal and navigate to the `backend` directory.
2. Copy the `.env.example` file to create a new `.env` file:
   ```bash
   cd backend
   cp .env.example .env
   ```
3. Open the new `.env` file. You don't need to change anything if you want to use the default SQLite setup (`sqlite:///credisphere.db`).

### 2. Backend Setup

Open a terminal and navigate to the `backend` directory.

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask API server
python app.py
```
*(The backend runs on `http://localhost:5000`)*

### 3. Frontend Setup

Open a new terminal window, navigate to the `frontend` directory, and start a simple HTTP server.

```bash
cd frontend
python3 -m http.server 5500
```

Open your browser and navigate to: [http://localhost:5500](http://localhost:5500)

## Features & Flows

### Customer Flow
1. **Signup/Login**: Role-based access with JWT and Isolation Forest simulated anomaly detection.
2. **Dashboard**: View XGBoost CrediScore and SHAP explanations.
3. **Loan Application**: Apply for loans with LightGBM eligibility estimation.
4. **KYC Upload**: Simulate EasyOCR and YOLOv8 for document verification.

### Admin Flow
1. **Dashboard**: Prophet/LSTM simulated forecasting for defaults and portfolio trends.
2. **Credit Intelligence**: XGBoost + GNN simulated default risk and fraud relationships.
3. **Collections AI**: Random Forest + Q-Learning simulated recovery strategies.
4. **Risk Policy**: Bayesian Optimization simulated thresholds.
5. **Screen Configuration**: Apriori widget recommendations.
