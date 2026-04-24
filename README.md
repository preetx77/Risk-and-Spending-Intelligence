````md
# 🎓 Student Finance Risk & Spending Intelligence System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green?style=for-the-badge&logo=scikitlearn)
![SQL](https://img.shields.io/badge/Database-SQL-orange?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<p align="center">
  <img src="docs/banner.png" alt="Project Banner" width="100%">
</p>

A **Data Mining & Warehousing project** focused on analyzing student spending behavior, predicting financial risks, detecting anomalies, and generating actionable insights using **machine learning, data warehousing, and dashboards**.

This system addresses **student financial mismanagement** by transforming raw transaction data into meaningful insights that support smarter financial decisions.

---

# 📌 Project Overview

Students often overspend, fail to monitor expenses, and gradually face financial stress. This project solves that problem through an intelligent analytics system that:

- Analyzes spending patterns
- Predicts overspending risks
- Detects unusual transactions
- Segments students by spending behavior
- Provides dashboard-based insights

The project combines **Data Warehousing** concepts like **ETL pipelines, star schema design, and OLAP structures** with **Data Mining algorithms** such as **K-Means, Random Forest, and Isolation Forest**.

---

# 🚀 Key Features

## ✨ Feature Highlights

| Feature | Description |
|--------|-------------|
| 📊 Spending Analysis | Tracks category-wise student expenses |
| ⚠️ Risk Prediction | Predicts overspending risks using ML |
| 🧠 Segmentation | Groups students by spending behavior |
| 🔍 Anomaly Detection | Flags unusual transactions |
| 📈 Dashboard | Interactive visual analytics |

---

## 📊 Spending Analysis

Tracks student spending across categories like food, rent, transport, shopping, and entertainment to identify spending trends.

## ⚠️ Risk Prediction

Uses **Random Forest** to predict whether a student is at risk of overspending based on spending patterns and transaction behavior.

## 🧠 Student Segmentation

Uses **K-Means Clustering** to group students into:

- High Spenders
- Moderate Spenders
- Budget Conscious Students

## 🔍 Anomaly Detection

Uses **Isolation Forest** to detect:

- Unusually high expenses
- Rare merchant usage
- Suspicious transactions

## 📈 Interactive Dashboard

Provides dashboards for:

- Spending trends
- Risk monitoring
- Cluster insights
- Transaction analysis

---

# 🏗️ System Architecture

```bash
Raw Data → Preprocessing → Feature Engineering → Data Warehouse → ML Models → Dashboard
````

### Workflow:

1. Load transaction data
2. Clean and preprocess records
3. Generate analytical features
4. Store data in warehouse schema
5. Train ML models
6. Visualize insights in dashboard

---

# 🗄️ Data Warehousing Design

The project uses a **Star Schema** for efficient analytics.

## Fact Table

`fact_transactions`

* transaction_id
* user_id
* category_id
* merchant_id
* payment_type_id
* amount
* date_id

## Dimension Tables

* `dim_users`
* `dim_date`
* `dim_category`
* `dim_merchant`
* `dim_payment_type`

This design supports fast queries, reporting, and OLAP analysis.

---

# 🤖 Machine Learning Models

## 1. K-Means Clustering

Segments students into spending groups.

## 2. Random Forest Classification

Predicts overspending risk.

### Performance:

* Accuracy: **87–90%**
* Precision: **85%**
* Recall: **83%**

## 3. Isolation Forest

Detects unusual or suspicious transactions.

---

# 📂 Project Structure

```bash
Risk-and-Spending-Intelligence/
│── data/
│── models/
│── notebooks/
│── src/
│── dashboard/
│── reports/
│── requirements.txt
│── README.md
```

---

# 🛠️ Tech Stack

* **Python**
* **Pandas / NumPy**
* **Scikit-learn**
* **Matplotlib / Plotly / Streamlit**
* **SQLite / SQL**

---

# 📊 Dashboard Modules

The dashboard includes:

* Overview analytics
* User analysis
* Cluster insights
* Risk monitoring
* Anomaly alerts

These modules convert raw analytics into easy-to-understand business intelligence.

---

# 📈 Business Impact

This project helps by:

* Improving student financial awareness
* Predicting overspending early
* Detecting anomalies quickly
* Supporting data-driven decisions

It demonstrates the real-world application of **Data Mining + Data Warehousing** in financial behavior analysis.

---

# ▶️ How to Run

## Clone the Repository

```bash
git clone https://github.com/preetx77/Risk-and-Spending-Intelligence.git
cd Risk-and-Spending-Intelligence
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📚 Academic Relevance

This project demonstrates:

* ETL pipeline implementation
* Star schema warehousing
* Classification and clustering
* Anomaly detection
* Feature engineering

It is suitable for **Data Mining & Warehousing academic projects, presentations, and portfolio showcases**.

---

# 👨‍💻 Author

Developed as part of a **Data Mining & Warehousing project** to demonstrate how machine learning and warehousing can solve real-world student finance challenges.

---

⭐ If you found this project useful, consider starring the repository.

```
```
