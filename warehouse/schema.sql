-- ============================================================================
-- Student Finance Data Warehouse Schema
-- Star Schema Design for OLAP Operations
-- ============================================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_users;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_merchant;
DROP TABLE IF EXISTS dim_payment_type;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- Dimension: Users
CREATE TABLE dim_users (
    user_id VARCHAR(50) PRIMARY KEY,
    total_spend DECIMAL(10, 2),
    avg_spend DECIMAL(10, 2),
    transaction_count INTEGER,
    risk_level VARCHAR(20),
    cluster_id INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20),
    day INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    weekday_name VARCHAR(20),
    is_weekend BOOLEAN,
    quarter INTEGER,
    UNIQUE(full_date)
);

-- Dimension: Category
CREATE TABLE dim_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) NOT NULL,
    category_type VARCHAR(50),
    description TEXT,
    UNIQUE(category_name)
);

-- Dimension: Merchant
CREATE TABLE dim_merchant (
    merchant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_name VARCHAR(200) NOT NULL,
    merchant_category VARCHAR(100),
    UNIQUE(merchant_name)
);

-- Dimension: Payment Type
CREATE TABLE dim_payment_type (
    payment_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_type_name VARCHAR(50) NOT NULL,
    is_digital BOOLEAN,
    UNIQUE(payment_type_name)
);

-- ============================================================================
-- FACT TABLE
-- ============================================================================

-- Fact: Transactions
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) NOT NULL,
    date_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    merchant_id INTEGER NOT NULL,
    payment_type_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (category_id) REFERENCES dim_category(category_id),
    FOREIGN KEY (merchant_id) REFERENCES dim_merchant(merchant_id),
    FOREIGN KEY (payment_type_id) REFERENCES dim_payment_type(payment_type_id)
);

-- ============================================================================
-- INDEXES for Performance Optimization
-- ============================================================================

-- Fact table indexes
CREATE INDEX idx_fact_user ON fact_transactions(user_id);
CREATE INDEX idx_fact_date ON fact_transactions(date_id);
CREATE INDEX idx_fact_category ON fact_transactions(category_id);
CREATE INDEX idx_fact_merchant ON fact_transactions(merchant_id);
CREATE INDEX idx_fact_amount ON fact_transactions(amount);

-- Date dimension indexes
CREATE INDEX idx_date_year_month ON dim_date(year, month);
CREATE INDEX idx_date_weekday ON dim_date(weekday);

-- User dimension indexes
CREATE INDEX idx_user_cluster ON dim_users(cluster_id);
CREATE INDEX idx_user_risk ON dim_users(risk_level);

-- ============================================================================
-- VIEWS for Common Queries
-- ============================================================================

-- View: Transaction Details
CREATE VIEW vw_transaction_details AS
SELECT 
    f.transaction_id,
    f.user_id,
    u.cluster_id,
    u.risk_level,
    d.full_date,
    d.year,
    d.month,
    d.weekday_name,
    d.is_weekend,
    c.category_name,
    m.merchant_name,
    p.payment_type_name,
    f.amount
FROM fact_transactions f
JOIN dim_users u ON f.user_id = u.user_id
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_category c ON f.category_id = c.category_id
JOIN dim_merchant m ON f.merchant_id = m.merchant_id
JOIN dim_payment_type p ON f.payment_type_id = p.payment_type_id;

-- View: User Spending Summary
CREATE VIEW vw_user_spending_summary AS
SELECT 
    u.user_id,
    u.total_spend,
    u.avg_spend,
    u.transaction_count,
    u.cluster_id,
    u.risk_level,
    COUNT(f.transaction_id) as actual_transaction_count,
    SUM(f.amount) as actual_total_spend,
    AVG(f.amount) as actual_avg_spend
FROM dim_users u
LEFT JOIN fact_transactions f ON u.user_id = f.user_id
GROUP BY u.user_id;

-- View: Category Performance
CREATE VIEW vw_category_performance AS
SELECT 
    c.category_name,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_revenue,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as unique_users
FROM fact_transactions f
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY c.category_name;

-- View: Monthly Trends
CREATE VIEW vw_monthly_trends AS
SELECT 
    d.year,
    d.month,
    d.month_name,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_spending,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as active_users
FROM fact_transactions f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- ============================================================================
-- MATERIALIZED AGGREGATES (Simulated with Tables)
-- ============================================================================

-- Daily Aggregates
CREATE TABLE agg_daily_spending AS
SELECT 
    date_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM fact_transactions
GROUP BY date_id;

-- User-Category Aggregates
CREATE TABLE agg_user_category AS
SELECT 
    user_id,
    category_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_spent
FROM fact_transactions
GROUP BY user_id, category_id;

-- ============================================================================
-- COMMENTS
-- ============================================================================

-- Schema follows Kimball's dimensional modeling principles
-- Star schema optimized for OLAP queries
-- Indexes created on frequently queried columns
-- Views provide convenient access to common queries
-- Aggregates pre-computed for performance
