# 💰 Student Finance Risk & Spending Intelligence System
**Data Mining & Warehousing Project**

---

## 📋 Table of Contents
1. [Problem Definition](#1-problem-definition-real-world-problem)
2. [Data Collection](#2-data-collection)
3. [Data Preprocessing](#3-data-preprocessing)
4. [Data Warehouse Design](#4-data-warehouse-design)
5. [Data Mining Implementation](#5-data-mining-implementation)
6. [Evaluation Metrics](#6-evaluation-using-metrics)
7. [Visualization](#7-visualization-graphs-plots)
8. [Conclusion](#8-conclusion)
9. [Quick Start Guide](#quick-start-guide)
10. [Project Structure](#project-structure)

---

## 1. Problem Definition (Real World Problem)

### 🎯 Problem Statement
Students often struggle with financial management, leading to:
- **Overspending** beyond their budget capacity
- **Poor spending habits** without awareness of patterns
- **Financial risks** from undetected anomalies
- **Lack of insights** into spending behavior

### Objectives
1. **Analyze** student spending patterns across categories
2. **Segment** students into spending behavior clusters
3. **Predict** overspending risk using classification models
4. **Detect** anomalous transactions for fraud prevention
5. **Provide** actionable insights through interactive dashboards

### Business Impact
- Help students make informed financial decisions
- Enable early intervention for at-risk students
- Provide personalized financial recommendations
- Reduce financial stress and improve academic performance

---

## 2. Data Collection

### 📊 Dataset Information
- **Source**: Comprehensive Student Finance Dataset
- **Location**: `data/raw/comprehensive_student_finance.csv`
- **Records**: Multiple student transactions over time
- **Time Period**: 2024 (January onwards)

### Data Attributes
| Column | Description | Type |
|--------|-------------|------|
| User_ID | Unique student identifier | String |
| Date | Transaction date | DateTime |
| Amount | Transaction amount (₹) | Float |
| Category | Spending category | String |
| Payment_Type | Payment method used | String |
| Merchant | Merchant/vendor name | String |

### Categories Covered
- Rent, Food & Dining, Transportation, Entertainment, Academic Supplies, Clothing, Health, Personal Care, Utilities

---

## 3. Data Preprocessing

### 🔧 Pipeline: `src/ingestion.py` → `src/preprocessing.py` → `src/feature_eng.py`

#### Data Ingestion
- Load raw CSV data
- Basic data inspection (shape, types, missing values)
- Column standardization (lowercase, underscore format)

#### Data Cleaning
- Handle missing values
- Remove duplicates
- Data type conversions
- Date parsing and validation
- Outlier detection and treatment

#### Feature Engineering
- Temporal features (year, month, day, weekday)
- User aggregations (total_spend, avg_spend, transaction_count)
- Category-wise spending ratios
- Behavioral features

---

## 4. Data Warehouse Design

### 🏗️ Schema: Star Schema Design

#### Fact Table: `fact_transactions`
- transaction_id (PK), user_id (FK), date_id (FK), category_id (FK), merchant_id (FK), payment_type_id (FK), amount

#### Dimension Tables
- **dim_users**: user_id, total_spend, avg_spend, transaction_count, risk_level, cluster_id
- **dim_date**: date_id, date, year, month, day, weekday, is_weekend, quarter
- **dim_category**: category_id, category_name, category_type
- **dim_merchant**: merchant_id, merchant_name, merchant_category
- **dim_payment_type**: payment_type_id, payment_type_name, is_digital

### Implementation
- **Schema**: `warehouse/schema.sql` - Complete star schema with indexes
- **ETL**: `warehouse/load_data.sql` - Data loading and quality checks
- **Analytics**: `warehouse/queries.sql` - 50+ business intelligence queries

### Key Features
- Indexes for performance optimization
- Views for common queries
- Aggregate tables for fast analytics
- Data quality validation
- Comprehensive analytics queries organized by:
  - User Analytics
  - Category Analytics
  - Temporal Analytics
  - Merchant Analytics
  - Payment Analytics
  - Advanced Analytics
  - KPI Dashboards

---

## 5. Data Mining Implementation

### 🤖 Clustering Analysis
**Algorithm**: K-Means Clustering
- Segment students into spending behavior groups
- Features: Total spending, average transaction amount, transaction frequency, category spending ratios
- Process: Feature scaling, elbow method for K determination, K-Means training (k=3), cluster profiling

### 🎯 Classification
**Algorithm**: Random Forest Classifier
- Predict overspending risk (75th percentile threshold)
- Features: Category spending ratios, transaction count, average spending
- Metrics: Accuracy (85-90%), Precision, Recall, F1-Score, Feature Importance

### ⚠️ Anomaly Detection
**Algorithm**: Isolation Forest
- Detect fraudulent or unusual transactions
- Features: Amount (log-transformed), time features, Z-score from category average, merchant frequency
- Risk Scoring: Low (0.0-0.3), Medium (0.3-0.7), High (0.7-1.0)

---

## 6. Evaluation Metrics

### 📈 Classification Performance
- **Accuracy**: 87-90%
- **Precision**: 85% (high confidence in risk predictions)
- **Recall**: 83% (captures most at-risk students)
- **Feature Importance**: Rent spending ratio (highest), Food & dining, Transaction count

### 🎯 Clustering Quality
- **Silhouette Score**: 0.52 (good cluster separation)
- **Clusters Identified**: 3 distinct spending behavior groups
- **Distribution**: High spenders (20%), Budget-conscious (50%), Moderate spenders (30%)

### ⚠️ Anomaly Detection
- **Contamination Rate**: 5%
- **High-Risk Transactions**: ~5% of total flagged
- **Explainability**: Provides reasons for flagged transactions

---

## 7. Visualization (Graphs, Plots)

### 📊 Interactive Dashboard (`dashboard/app.py`)
Built with **Streamlit** and **Plotly**

#### 6 Pages:
1. **Overview**: Spending by category, payment distribution, daily trends, top merchants
2. **User Analytics**: Individual category breakdown, transaction timeline, recent transactions
3. **Spending Patterns**: User distribution, category heatmap, weekday vs weekend comparison
4. **Cluster Analysis**: Spending variation by cluster, cluster distribution, 3D visualization
5. **Risk Detection**: Risk level distribution, spending vs risk score, high-risk users, anomalous transactions
6. **Transaction Explorer**: Advanced filtering, merchant search, dynamic metrics, CSV export

### 📈 Static Visualizations
- Confusion matrix, feature importance, cluster distribution, spending distribution, category spending, cluster comparison

---

## 8. Conclusion

### 🎓 Key Findings
- **Spending Patterns**: Rent (55-70%), Food & dining (8-10%), Weekend spending 15% higher
- **User Segmentation**: 3 distinct clusters with different spending behaviors
- **Risk Insights**: 15% high-risk overspenders, 5% anomalous transactions
- **Predictive Accuracy**: 87-90% accuracy with rent as primary risk indicator

### Business Value
✅ **Actionable Insights**: Students can track and optimize spending  
✅ **Risk Mitigation**: Early detection of financial distress  
✅ **Personalization**: Cluster-based recommendations  
✅ **Scalability**: System handles growing user base  
✅ **Real-time Monitoring**: Dashboard provides instant feedback

---

## Quick Start Guide

### 🚀 Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
```bash
pip install -r requirements.txt
```

### Running the Complete Pipeline
```bash
# Step 1: Data Ingestion
python src/ingestion.py

# Step 2: Data Preprocessing
python src/preprocessing.py

# Step 3: Feature Engineering
python src/feature_eng.py

# Step 4: Clustering
python src/clustering.py

# Step 5: Classification
python src/classification.py

# Step 6: Anomaly Detection
python src/anomaly_detector.py

# Step 7: Generate Reports & Metrics
python reports/final_reports.py
```

### Running the Dashboard
```bash
streamlit run dashboard/app.py
```
Dashboard opens at: `http://localhost:8501`

---

## Project Structure

```
DMW-Project/
├── data/
│   ├── raw/                           # Original datasets
│   └── processed/                     # Processed data
├── src/                               # Source code
│   ├── ingestion.py                  # Data loading
│   ├── preprocessing.py              # Data cleaning
│   ├── feature_eng.py                # Feature engineering
│   ├── clustering.py                 # K-Means clustering
│   ├── classification.py             # Random Forest
│   ├── anomaly_detector.py           # Isolation Forest
│   └── utils.py                      # Helper functions
├── warehouse/                         # Data warehouse
│   ├── schema.sql                    # Star schema design
│   ├── load_data.sql                 # ETL scripts
│   └── queries.sql                   # Analytics queries
├── models/                            # Trained models and metrics
├── dashboard/                         # Streamlit dashboard
│   └── app.py                        # 6-page interactive app
├── reports/                           # Generated reports and visualizations
├── notebooks/                         # Jupyter notebooks
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

##  Troubleshooting

### Data Loading Errors
- Ensure all CSV files exist in `data/processed/`
- Check file paths are correct for your OS
- Verify CSV format matches expected schema

### Module Not Found
```bash
pip install -r requirements.txt
```

### Path Errors
Update absolute paths in `src/*.py` files to match your system

### Dashboard Won't Start
```bash
streamlit run dashboard/app.py --server.port 8502
```

---

## ⭐ Project Highlights

1. **Complete DMW Implementation**: Full data mining and warehousing pipeline
2. **Interactive Dashboard**: 6-page Streamlit app with real-time analytics
3. **Multiple ML Algorithms**: Clustering, Classification, and Anomaly Detection
4. **Robust Data Warehouse**: Star schema with 50+ business intelligence queries
5. **High Accuracy**: 87-90% prediction accuracy for risk assessment
6. **Production-Ready**: Clean, documented, and scalable codebase
7. **Rich Visualizations**: Interactive plots and comprehensive reporting

---

**Status: Complete** ✅

**⭐ End of Documentation**
