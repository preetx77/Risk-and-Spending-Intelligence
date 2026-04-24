# Student Finance Risk & Spending Intelligence System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Machine_Learning-Scikit--learn-green?style=for-the-badge&logo=scikitlearn)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange?style=for-the-badge&logo=sqlite)

A **Data Mining & Warehousing** academic project that analyzes student spending behavior, predicts financial overspending risk, detects anomalous transactions, and segments students by financial profile — all surfaced through an interactive Streamlit dashboard.

---

## Overview

Students frequently overspend without realizing it until it's too late. This system converts raw transaction data into actionable financial intelligence using a combination of **ETL pipelines**, **star schema data warehousing**, and **machine learning models** (K-Means, Random Forest, Isolation Forest).

---

## Features

| Feature | Description |
|---|---|
| Spending Analysis | Category-wise expense tracking across food, rent, transport, shopping, and entertainment |
| Risk Prediction | Random Forest classifier to flag students at risk of overspending |
| Student Segmentation | K-Means clustering to group students by spending behavior |
| Anomaly Detection | Isolation Forest to surface unusual or suspicious transactions |
| Interactive Dashboard | Streamlit-based visual analytics across all modules |

---

## System Architecture

```
Raw Transaction Data
       ↓
  Preprocessing & Cleaning
       ↓
  Feature Engineering
       ↓
  Data Warehouse (Star Schema / SQLite)
       ↓
  ML Model Training (K-Means / Random Forest / Isolation Forest)
       ↓
  Streamlit Dashboard
```

---

## Data Warehouse Design

Uses a **Star Schema** for OLAP-compatible analytics.

**Fact Table:** `fact_transactions`
- `transaction_id`, `user_id`, `category_id`, `merchant_id`, `payment_type_id`, `amount`, `date_id`

**Dimension Tables:**
- `dim_users`
- `dim_date`
- `dim_category`
- `dim_merchant`
- `dim_payment_type`

---

## Machine Learning Models

### 1. K-Means Clustering
Groups students into three spending segments:
- High Spenders
- Moderate Spenders
- Budget-Conscious Students

### 2. Random Forest Classifier
Predicts overspending risk based on transaction patterns.

| Metric | Score |
|---|---|
| Accuracy | 87–90% |
| Precision | 85% |
| Recall | 83% |

### 3. Isolation Forest
Detects outlier transactions — unusually high amounts, rare merchants, or suspicious patterns.

---

## Project Structure

```
Risk-and-Spending-Intelligence/
├── data/               # Raw and processed datasets
├── models/             # Trained ML model artifacts
├── notebooks/          # Exploratory analysis and experimentation
├── src/                # Core pipeline scripts (ETL, feature engineering, modeling)
├── dashboard/          # Streamlit app
├── reports/            # Output reports and visualizations
├── requirements.txt
└── README.md
```

---

## Tech Stack

- **Python 3.x**
- **Pandas / NumPy** — data processing
- **Scikit-learn** — ML models
- **Matplotlib / Plotly** — visualization
- **Streamlit** — dashboard
- **SQLite / SQL** — data warehouse

---

## Dashboard Modules

- **Overview** — aggregate spending summary
- **User Analysis** — per-student transaction breakdown
- **Cluster Insights** — spending segment profiles
- **Risk Monitoring** — overspending predictions
- **Anomaly Alerts** — flagged suspicious transactions

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/preetx77/Risk-and-Spending-Intelligence.git
cd Risk-and-Spending-Intelligence

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run dashboard/app.py
```

---

## Academic Scope

This project demonstrates the following concepts from a **Data Mining & Warehousing** curriculum:

- ETL pipeline design and implementation
- Star schema dimensional modeling
- Supervised classification (Random Forest)
- Unsupervised clustering (K-Means)
- Outlier detection (Isolation Forest)
- Feature engineering from transactional data

---

## Author

Developed as a **Data Mining & Warehousing** academic project.  
GitHub: [@preetx77](https://github.com/preetx77)
