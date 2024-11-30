-- Create tables for the financial data

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    userid VARCHAR(6) NOT NULL,
    spending_amount DECIMAL(10,2) NOT NULL,
    receipient_category VARCHAR(50) NOT NULL,
    necessities_or_non_essential BOOLEAN NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- Create financial_metrics table
CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_id SERIAL PRIMARY KEY,
    userid VARCHAR(6) NOT NULL,
    cancellation_rate DECIMAL(4,2),
    ratings DECIMAL(4,2),
    responsiveness_to_task DECIMAL(4,2),
    min_max_diff_past_6_months DECIMAL(4,2),
    ratings_influx DECIMAL(4,2),
    type_of_gig VARCHAR(20),
    social_media_activeness_score DECIMAL(4,2),
    permanent_employment VARCHAR(3),
    years_of_employment INTEGER,
    fluctuation_rate DECIMAL(4,2),
    gross_income DECIMAL(10,2),
    net_income DECIMAL(10,2),
    impulsive_purchase_rate DECIMAL(5,2),
    recurring_expense_consistency DECIMAL(5,2),
    expense_to_income_ratio DECIMAL(5,2),
    regular_saving BOOLEAN,
    regular_savings_amount DECIMAL(10,2),
    emergency_fund_availability BOOLEAN,
    emergency_fund_amount DECIMAL(10,2),
    consistent_spending BOOLEAN,
    spending_amount DECIMAL(10,2),
    portfolio_diversification_risk DECIMAL(4,2),
    awareness_of_utilisation_of_pfm INTEGER,
    timestamp TIMESTAMP NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX idx_transactions_userid ON transactions(userid);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX idx_financial_metrics_userid ON financial_metrics(userid);
CREATE INDEX idx_financial_metrics_timestamp ON financial_metrics(timestamp);

-- Copy data from CSV files
COPY transactions(userid, spending_amount, receipient_category, necessities_or_non_essential, timestamp) 
FROM '/Users/haoming/Documents/PayHack 2024/ninjakakiData/transaction.csv' 
DELIMITER ',' CSV HEADER;

COPY financial_metrics(userid, cancellation_rate, ratings, responsiveness_to_task, min_max_diff_past_6_months, 
    ratings_influx, type_of_gig, social_media_activeness_score, permanent_employment, years_of_employment, 
    fluctuation_rate, gross_income, net_income, impulsive_purchase_rate, recurring_expense_consistency, 
    expense_to_income_ratio, regular_saving, regular_savings_amount, emergency_fund_availability, 
    emergency_fund_amount, consistent_spending, spending_amount, portfolio_diversification_risk, 
    awareness_of_utilisation_of_pfm, timestamp) 
FROM '/Users/haoming/Documents/PayHack 2024/ninjakakiData/merged.csv' 
DELIMITER ',' CSV HEADER;
