-- ============================================================================
-- Analytics Queries for Student Finance Data Warehouse
-- Business Intelligence and Reporting Queries
-- ============================================================================

-- ============================================================================
-- SECTION 1: User Analytics
-- ============================================================================

-- Query 1.1: Top 10 Spenders
SELECT 
    u.user_id,
    u.total_spend,
    u.transaction_count,
    u.avg_spend,
    u.cluster_id,
    u.risk_level
FROM dim_users u
ORDER BY u.total_spend DESC
LIMIT 10;

-- Query 1.2: User Spending by Cluster
SELECT 
    cluster_id,
    COUNT(*) as user_count,
    AVG(total_spend) as avg_total_spend,
    MIN(total_spend) as min_spend,
    MAX(total_spend) as max_spend,
    AVG(transaction_count) as avg_transactions
FROM dim_users
GROUP BY cluster_id
ORDER BY cluster_id;

-- Query 1.3: Risk Level Distribution
SELECT 
    risk_level,
    COUNT(*) as user_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dim_users), 2) as percentage,
    AVG(total_spend) as avg_spend
FROM dim_users
GROUP BY risk_level
ORDER BY 
    CASE risk_level
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;

-- ============================================================================
-- SECTION 2: Category Analytics
-- ============================================================================

-- Query 2.1: Category Performance Summary
SELECT 
    c.category_name,
    c.category_type,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_revenue,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as unique_users,
    ROUND(SUM(f.amount) * 100.0 / (SELECT SUM(amount) FROM fact_transactions), 2) as revenue_percentage
FROM fact_transactions f
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY c.category_name, c.category_type
ORDER BY total_revenue DESC;

-- Query 2.2: Category Spending by User Cluster
SELECT 
    u.cluster_id,
    c.category_name,
    COUNT(f.transaction_id) as transactions,
    SUM(f.amount) as total_spent,
    AVG(f.amount) as avg_spent
FROM fact_transactions f
JOIN dim_users u ON f.user_id = u.user_id
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY u.cluster_id, c.category_name
ORDER BY u.cluster_id, total_spent DESC;

-- Query 2.3: Essential vs Discretionary Spending
SELECT 
    c.category_type,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_amount,
    AVG(f.amount) as avg_amount,
    ROUND(SUM(f.amount) * 100.0 / (SELECT SUM(amount) FROM fact_transactions), 2) as percentage
FROM fact_transactions f
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY c.category_type
ORDER BY total_amount DESC;

-- ============================================================================
-- SECTION 3: Temporal Analytics
-- ============================================================================

-- Query 3.1: Monthly Spending Trends
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

-- Query 3.2: Weekday vs Weekend Spending
SELECT 
    CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END as day_type,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_spending,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as unique_users
FROM fact_transactions f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.is_weekend;

-- Query 3.3: Daily Spending Pattern
SELECT 
    d.weekday_name,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_spending,
    AVG(f.amount) as avg_transaction
FROM fact_transactions f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.weekday, d.weekday_name
ORDER BY d.weekday;

-- Query 3.4: Quarterly Performance
SELECT 
    d.year,
    d.quarter,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_revenue,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as active_users
FROM fact_transactions f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;

-- ============================================================================
-- SECTION 4: Merchant Analytics
-- ============================================================================

-- Query 4.1: Top 20 Merchants by Revenue
SELECT 
    m.merchant_name,
    m.merchant_category,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_revenue,
    AVG(f.amount) as avg_transaction,
    COUNT(DISTINCT f.user_id) as unique_customers
FROM fact_transactions f
JOIN dim_merchant m ON f.merchant_id = m.merchant_id
GROUP BY m.merchant_name, m.merchant_category
ORDER BY total_revenue DESC
LIMIT 20;

-- Query 4.2: Merchant Diversity by User
SELECT 
    f.user_id,
    COUNT(DISTINCT f.merchant_id) as unique_merchants,
    COUNT(f.transaction_id) as total_transactions,
    SUM(f.amount) as total_spent
FROM fact_transactions f
GROUP BY f.user_id
ORDER BY unique_merchants DESC
LIMIT 20;

-- ============================================================================
-- SECTION 5: Payment Analytics
-- ============================================================================

-- Query 5.1: Payment Method Distribution
SELECT 
    p.payment_type_name,
    p.is_digital,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_amount,
    AVG(f.amount) as avg_amount,
    ROUND(COUNT(f.transaction_id) * 100.0 / (SELECT COUNT(*) FROM fact_transactions), 2) as usage_percentage
FROM fact_transactions f
JOIN dim_payment_type p ON f.payment_type_id = p.payment_type_id
GROUP BY p.payment_type_name, p.is_digital
ORDER BY transaction_count DESC;

-- Query 5.2: Digital vs Cash Payments
SELECT 
    CASE WHEN p.is_digital = 1 THEN 'Digital' ELSE 'Cash' END as payment_mode,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.amount) as total_amount,
    AVG(f.amount) as avg_amount
FROM fact_transactions f
JOIN dim_payment_type p ON f.payment_type_id = p.payment_type_id
GROUP BY p.is_digital;

-- ============================================================================
-- SECTION 6: Advanced Analytics
-- ============================================================================

-- Query 6.1: User Cohort Analysis (by spending level)
SELECT 
    CASE 
        WHEN total_spend < 2000 THEN 'Low Spender'
        WHEN total_spend BETWEEN 2000 AND 4000 THEN 'Medium Spender'
        ELSE 'High Spender'
    END as spending_cohort,
    COUNT(*) as user_count,
    AVG(total_spend) as avg_spend,
    AVG(transaction_count) as avg_transactions,
    AVG(avg_spend) as avg_transaction_size
FROM dim_users
GROUP BY spending_cohort;

-- Query 6.2: Category Affinity Analysis
SELECT 
    c1.category_name as category_1,
    c2.category_name as category_2,
    COUNT(DISTINCT f1.user_id) as common_users,
    AVG(f1.amount + f2.amount) as avg_combined_spend
FROM fact_transactions f1
JOIN fact_transactions f2 ON f1.user_id = f2.user_id AND f1.category_id < f2.category_id
JOIN dim_category c1 ON f1.category_id = c1.category_id
JOIN dim_category c2 ON f2.category_id = c2.category_id
GROUP BY c1.category_name, c2.category_name
HAVING common_users > 5
ORDER BY common_users DESC
LIMIT 20;

-- Query 6.3: High-Value Transaction Analysis
SELECT 
    f.user_id,
    u.risk_level,
    d.full_date,
    c.category_name,
    m.merchant_name,
    f.amount,
    ROUND((f.amount - AVG(f.amount) OVER ()) / NULLIF(STDDEV(f.amount) OVER (), 0), 2) as z_score
FROM fact_transactions f
JOIN dim_users u ON f.user_id = u.user_id
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_category c ON f.category_id = c.category_id
JOIN dim_merchant m ON f.merchant_id = m.merchant_id
WHERE f.amount > (SELECT AVG(amount) + 2 * STDDEV(amount) FROM fact_transactions)
ORDER BY f.amount DESC;

-- Query 6.4: User Retention Analysis (Active vs Inactive)
SELECT 
    u.user_id,
    u.total_spend,
    COUNT(f.transaction_id) as recent_transactions,
    MAX(d.full_date) as last_transaction_date,
    julianday('now') - julianday(MAX(d.full_date)) as days_since_last_transaction,
    CASE 
        WHEN julianday('now') - julianday(MAX(d.full_date)) <= 7 THEN 'Active'
        WHEN julianday('now') - julianday(MAX(d.full_date)) <= 30 THEN 'At Risk'
        ELSE 'Inactive'
    END as user_status
FROM dim_users u
LEFT JOIN fact_transactions f ON u.user_id = f.user_id
LEFT JOIN dim_date d ON f.date_id = d.date_id
GROUP BY u.user_id, u.total_spend
ORDER BY days_since_last_transaction;

-- ============================================================================
-- SECTION 7: KPI Dashboard Queries
-- ============================================================================

-- Query 7.1: Executive Summary
SELECT 
    (SELECT COUNT(*) FROM dim_users) as total_users,
    (SELECT COUNT(*) FROM fact_transactions) as total_transactions,
    (SELECT SUM(amount) FROM fact_transactions) as total_revenue,
    (SELECT AVG(amount) FROM fact_transactions) as avg_transaction_value,
    (SELECT COUNT(DISTINCT user_id) FROM fact_transactions) as active_users,
    (SELECT COUNT(*) FROM dim_merchant) as total_merchants,
    (SELECT COUNT(*) FROM dim_category) as total_categories;

-- Query 7.2: Risk Summary
SELECT 
    risk_level,
    COUNT(*) as user_count,
    SUM(total_spend) as total_spend,
    AVG(total_spend) as avg_spend
FROM dim_users
GROUP BY risk_level;

-- Query 7.3: Growth Metrics (Month-over-Month)
WITH monthly_stats AS (
    SELECT 
        d.year,
        d.month,
        SUM(f.amount) as monthly_revenue,
        COUNT(f.transaction_id) as monthly_transactions,
        COUNT(DISTINCT f.user_id) as monthly_active_users
    FROM fact_transactions f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month
)
SELECT 
    year,
    month,
    monthly_revenue,
    monthly_transactions,
    monthly_active_users,
    LAG(monthly_revenue) OVER (ORDER BY year, month) as prev_month_revenue,
    ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year, month)) * 100.0 / 
          NULLIF(LAG(monthly_revenue) OVER (ORDER BY year, month), 0), 2) as revenue_growth_pct
FROM monthly_stats
ORDER BY year, month;

-- ============================================================================
-- End of Analytics Queries
-- ============================================================================
