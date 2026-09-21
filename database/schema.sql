CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'CUSTOMER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    phone VARCHAR(20),
    address TEXT,
    employment_status VARCHAR(50),
    annual_income NUMERIC(15, 2),
    credit_score INTEGER DEFAULT 0,
    kyc_status VARCHAR(20) DEFAULT 'PENDING'
);

CREATE TABLE IF NOT EXISTS kyc_documents (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    document_type VARCHAR(50),
    document_url VARCHAR(255),
    verification_status VARCHAR(20) DEFAULT 'PENDING',
    ocr_data JSONB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    amount NUMERIC(15, 2) NOT NULL,
    purpose VARCHAR(100),
    term_months INTEGER,
    interest_rate NUMERIC(5, 2),
    status VARCHAR(20) DEFAULT 'PENDING',
    ai_recommendation VARCHAR(20),
    ai_confidence NUMERIC(5, 2),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS credit_decisions (
    id SERIAL PRIMARY KEY,
    loan_id INTEGER REFERENCES loans(id) ON DELETE CASCADE,
    decision VARCHAR(20),
    decision_reason TEXT,
    shap_explanation JSONB,
    decided_by INTEGER REFERENCES users(id),
    decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collection_cases (
    id SERIAL PRIMARY KEY,
    loan_id INTEGER REFERENCES loans(id) ON DELETE CASCADE,
    outstanding_amount NUMERIC(15, 2),
    days_overdue INTEGER,
    recovery_probability NUMERIC(5, 2),
    recommended_strategy VARCHAR(100),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
