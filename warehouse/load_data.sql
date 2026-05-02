-- # PREET SONAR 
-- # PRN : 20240802258

-- Load dim_date
INSERT INTO dim_date (date_id, full_date, year, month, month_name, day, weekday, weekday_name, is_weekend, quarter)
SELECT DISTINCT
    CAST(strftime('%Y%m%d', Date) AS INTEGER) as date_id,
    Date as full_date,
    year,
    month,
    CASE month
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END as month_name,
    day,
    weekday,
    CASE weekday
        WHEN 0 THEN 'Monday'
        WHEN 1 THEN 'Tuesday'
        WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday'
        WHEN 4 THEN 'Friday'
        WHEN 5 THEN 'Saturday'
        WHEN 6 THEN 'Sunday'
    END as weekday_name,
    CASE WHEN weekday IN (5, 6) THEN 1 ELSE 0 END as is_weekend,
    CASE 
        WHEN month IN (1,2,3) THEN 1
        WHEN month IN (4,5,6) THEN 2
        WHEN month IN (7,8,9) THEN 3
        ELSE 4
    END as quarter
FROM cleaned_transactions;

-- Load dim_category
INSERT INTO dim_category (category_name, category_type)
SELECT DISTINCT
    Category as category_name,
    CASE 
        WHEN Category IN ('rent', 'utilities') THEN 'Essential'
        WHEN Category IN ('food & dining') THEN 'Necessary'
        WHEN Category IN ('entertainment', 'clothing') THEN 'Discretionary'
        WHEN Category IN ('academic supplies') THEN 'Educational'
        WHEN Category IN ('health', 'personal care') THEN 'Healthcare'
        WHEN Category IN ('transportation') THEN 'Transport'
        ELSE 'Other'
    END as category_type
FROM cleaned_transactions;

-- Load dim_merchant
INSERT INTO dim_merchant (merchant_name, merchant_category)
SELECT DISTINCT
    Merchant as merchant_name,
    Category as merchant_category
FROM cleaned_transactions;

-- Load dim_payment_type
INSERT INTO dim_payment_type (payment_type_name, is_digital)
SELECT DISTINCT
    Payment_Type as payment_type_name,
    CASE 
        WHEN Payment_Type IN ('digital wallet', 'credit card', 'debit card') THEN 1
        ELSE 0
    END as is_digital
FROM cleaned_transactions;

-- Load dim_users (from features and clusters)
INSERT INTO dim_users (user_id, total_spend, avg_spend, transaction_count, risk_level, cluster_id)
SELECT 
    c.User_ID,
    c.total_spend,
    c.avg_spend,
    c.transaction_count,
    CASE 
        WHEN c.total_spend > (SELECT AVG(total_spend) + 1.5 * (SELECT AVG(total_spend) FROM clusters) FROM clusters) THEN 'High'
        WHEN c.total_spend > (SELECT AVG(total_spend) FROM clusters) THEN 'Medium'
        ELSE 'Low'
    END as risk_level,
    c.cluster
FROM clusters c;

-- ============================================================================
-- STEP 2: Load Fact Table
-- ============================================================================

INSERT INTO fact_transactions (user_id, date_id, category_id, merchant_id, payment_type_id, amount)
SELECT 
    ct.User_ID,
    CAST(strftime('%Y%m%d', ct.Date) AS INTEGER) as date_id,
    dc.category_id,
    dm.merchant_id,
    dp.payment_type_id,
    ct.Amount
FROM cleaned_transactions ct
JOIN dim_category dc ON ct.Category = dc.category_name
JOIN dim_merchant dm ON ct.Merchant = dm.merchant_name
JOIN dim_payment_type dp ON ct.Payment_Type = dp.payment_type_name;

-- ============================================================================
-- STEP 3: Verify Data Load
-- ============================================================================

-- Check record counts
SELECT 'dim_users' as table_name, COUNT(*) as record_count FROM dim_users
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'dim_category', COUNT(*) FROM dim_category
UNION ALL
SELECT 'dim_merchant', COUNT(*) FROM dim_merchant
UNION ALL
SELECT 'dim_payment_type', COUNT(*) FROM dim_payment_type
UNION ALL
SELECT 'fact_transactions', COUNT(*) FROM fact_transactions;

-- ============================================================================
-- STEP 4: Data Quality Checks
-- ============================================================================

-- Check for orphaned records in fact table
SELECT 'Orphaned User Records' as check_type, COUNT(*) as count
FROM fact_transactions f
LEFT JOIN dim_users u ON f.user_id = u.user_id
WHERE u.user_id IS NULL

UNION ALL

SELECT 'Orphaned Date Records', COUNT(*)
FROM fact_transactions f
LEFT JOIN dim_date d ON f.date_id = d.date_id
WHERE d.date_id IS NULL

UNION ALL

SELECT 'Orphaned Category Records', COUNT(*)
FROM fact_transactions f
LEFT JOIN dim_category c ON f.category_id = c.category_id
WHERE c.category_id IS NULL;

-- Check for negative amounts
SELECT 'Negative Amounts' as check_type, COUNT(*) as count
FROM fact_transactions
WHERE amount < 0;

-- Check for NULL values in critical fields
SELECT 'NULL User IDs' as check_type, COUNT(*) as count
FROM fact_transactions
WHERE user_id IS NULL

UNION ALL

SELECT 'NULL Amounts', COUNT(*)
FROM fact_transactions
WHERE amount IS NULL;

-- ============================================================================
-- STEP 5: Update Aggregate Tables
-- ============================================================================

-- Refresh daily aggregates
DELETE FROM agg_daily_spending;
INSERT INTO agg_daily_spending
SELECT 
    date_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM fact_transactions
GROUP BY date_id;

-- Refresh user-category aggregates
DELETE FROM agg_user_category;
INSERT INTO agg_user_category
SELECT 
    user_id,
    category_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_spent
FROM fact_transactions
GROUP BY user_id, category_id;

-- ============================================================================
-- ETL Complete
-- ============================================================================

SELECT 'ETL Process Completed Successfully' as status;
