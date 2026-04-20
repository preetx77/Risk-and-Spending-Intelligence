"""
Risk & Spending Intelligence Dashboard
Student Finance Analytics Platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Page config
st.set_page_config(
    page_title="Student Finance Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        margin: 0 0 10px 0;
        font-size: 20px;
    }
    .metric-card p {
        margin: 5px 0;
        font-size: 16px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Data loading with caching
@st.cache_data
def load_data():
    """Load all processed datasets"""
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    
    data = {
        'cleaned': pd.read_csv(os.path.join(base_path, 'cleaned.csv')),
        'features': pd.read_csv(os.path.join(base_path, 'features.csv')),
        'clusters': pd.read_csv(os.path.join(base_path, 'clusters.csv'))
    }
    
    # Convert date column
    data['cleaned']['Date'] = pd.to_datetime(data['cleaned']['Date'])
    
    return data

# Load data
try:
    data = load_data()
    df_transactions = data['cleaned']
    df_features = data['features']
    df_clusters = data['clusters']
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Overview", "👥 User Analytics", "📈 Spending Patterns", 
     "🎯 Cluster Analysis", "⚠️ Risk Detection", "🔍 Transaction Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Dataset Info**
- Total Users: {df_features.shape[0]}
- Total Transactions: {df_transactions.shape[0]}
- Date Range: {df_transactions['Date'].min().strftime('%Y-%m-%d')} to {df_transactions['Date'].max().strftime('%Y-%m-%d')}
""")

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "🏠 Overview":
    st.title("💰 Student Finance Intelligence Dashboard")
    st.markdown("### Real-time insights into student spending patterns and financial risks")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_spend = df_transactions['Amount'].sum()
    avg_transaction = df_transactions['Amount'].mean()
    total_users = df_features.shape[0]
    total_transactions = df_transactions.shape[0]
    
    with col1:
        st.metric(
            label="Total Spending",
            value=f"₹{total_spend:,.2f}",
            delta="All time"
        )
    
    with col2:
        st.metric(
            label="Avg Transaction",
            value=f"₹{avg_transaction:.2f}"
        )
    
    with col3:
        st.metric(
            label="Active Users",
            value=f"{total_users:,}"
        )
    
    with col4:
        st.metric(
            label="Total Transactions",
            value=f"{total_transactions:,}"
        )
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Spending by Category")
        category_spend = df_transactions.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=category_spend.values,
            names=category_spend.index,
            title="Category Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💳 Payment Methods")
        payment_dist = df_transactions['Payment_Type'].value_counts()
        fig = px.bar(
            x=payment_dist.index,
            y=payment_dist.values,
            title="Payment Type Distribution",
            labels={'x': 'Payment Type', 'y': 'Count'},
            color=payment_dist.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Spending over time
    st.subheader("📈 Spending Trends Over Time")
    daily_spend = df_transactions.groupby('Date')['Amount'].sum().reset_index()
    fig = px.line(
        daily_spend,
        x='Date',
        y='Amount',
        title="Daily Spending Pattern",
        labels={'Amount': 'Total Spending (₹)'}
    )
    fig.update_traces(line_color='#1f77b4', line_width=2)
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Top merchants
    st.subheader("🏪 Top 10 Merchants")
    top_merchants = df_transactions.groupby('Merchant')['Amount'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=top_merchants.values,
        y=top_merchants.index,
        orientation='h',
        title="Highest Revenue Merchants",
        labels={'x': 'Total Revenue (₹)', 'y': 'Merchant'},
        color=top_merchants.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: USER ANALYTICS
# ============================================================================
elif page == "👥 User Analytics":
    st.title("👥 User Analytics")
    
    # User selector
    selected_user = st.selectbox("Select User", df_features['User_ID'].unique())
    
    # Get user data
    user_features = df_features[df_features['User_ID'] == selected_user].iloc[0]
    user_transactions = df_transactions[df_transactions['User_ID'] == selected_user]
    
    # User metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_spend_val = user_features['total_spend']
    avg_spend_val = user_features['avg_spend']
    transaction_count_val = int(user_features['transaction_count'])
    cluster_id = df_clusters[df_clusters['User_ID'] == selected_user]['cluster'].values[0]
    
    with col1:
        st.metric(
            label="Total Spending",
            value=f"₹{total_spend_val:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Avg Transaction",
            value=f"₹{avg_spend_val:.2f}"
        )
    
    with col3:
        st.metric(
            label="Transaction Count",
            value=f"{transaction_count_val}"
        )
    
    with col4:
        st.metric(
            label="Spending Cluster",
            value=f"Group {cluster_id}"
        )
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Category Breakdown")
        # Get category columns
        category_cols = [col for col in df_features.columns if col not in ['User_ID', 'total_spend', 'avg_spend', 'transaction_count']]
        user_categories = user_features[category_cols]
        
        fig = px.bar(
            x=user_categories.values,
            y=user_categories.index,
            orientation='h',
            title="Spending Distribution by Category",
            labels={'x': 'Proportion', 'y': 'Category'},
            color=user_categories.values,
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Transaction Timeline")
        user_daily = user_transactions.groupby('Date')['Amount'].sum().reset_index()
        fig = px.scatter(
            user_daily,
            x='Date',
            y='Amount',
            size='Amount',
            title="Daily Spending Pattern",
            labels={'Amount': 'Spending (₹)'}
        )
        fig.update_traces(marker=dict(color='#ff7f0e', line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions
    st.subheader("🔖 Recent Transactions")
    recent = user_transactions.sort_values('Date', ascending=False).head(10)
    st.dataframe(
        recent[['Date', 'Amount', 'Category', 'Merchant', 'Payment_Type']],
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# PAGE 3: SPENDING PATTERNS
# ============================================================================
elif page == "📈 Spending Patterns":
    st.title("📈 Spending Pattern Analysis")
    
    # Spending distribution
    st.subheader("💵 Spending Distribution Across Users")
    fig = px.histogram(
        df_features,
        x='total_spend',
        nbins=30,
        title="User Spending Distribution",
        labels={'total_spend': 'Total Spending (₹)', 'count': 'Number of Users'},
        color_discrete_sequence=['#2ca02c']
    )
    fig.add_vline(x=df_features['total_spend'].median(), line_dash="dash", 
                  annotation_text="Median", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Category Spending Heatmap")
        category_cols = [col for col in df_features.columns if col not in ['User_ID', 'total_spend', 'avg_spend', 'transaction_count']]
        category_data = df_features[category_cols].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=category_data.values,
            y=category_data.index,
            orientation='h',
            title="Average Category Allocation",
            labels={'x': 'Average Proportion', 'y': 'Category'},
            color=category_data.values,
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Weekday vs Weekend Spending")
        df_transactions['is_weekend'] = df_transactions['weekday'].isin([5, 6])
        weekend_spend = df_transactions.groupby('is_weekend')['Amount'].agg(['sum', 'mean', 'count']).reset_index()
        weekend_spend['is_weekend'] = weekend_spend['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Total Spending', 'Avg Transaction'))
        
        fig.add_trace(
            go.Bar(x=weekend_spend['is_weekend'], y=weekend_spend['sum'], 
                   name='Total', marker_color='lightblue'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=weekend_spend['is_weekend'], y=weekend_spend['mean'], 
                   name='Average', marker_color='lightcoral'),
            row=1, col=2
        )
        
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly trends
    st.subheader("📆 Monthly Spending Trends")
    df_transactions['month_name'] = df_transactions['Date'].dt.strftime('%B')
    monthly_category = df_transactions.groupby(['month', 'Category'])['Amount'].sum().reset_index()
    
    fig = px.bar(
        monthly_category,
        x='month',
        y='Amount',
        color='Category',
        title="Monthly Spending by Category",
        labels={'month': 'Month', 'Amount': 'Total Spending (₹)'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 4: CLUSTER ANALYSIS
# ============================================================================
elif page == "🎯 Cluster Analysis":
    st.title("🎯 User Segmentation & Cluster Analysis")
    
    # Cluster overview
    cluster_summary = df_clusters.groupby('cluster').agg({
        'total_spend': ['mean', 'min', 'max'],
        'avg_spend': 'mean',
        'transaction_count': 'mean',
        'User_ID': 'count'
    }).round(2)
    
    st.subheader("📊 Cluster Summary")
    
    # Display cluster metrics
    num_clusters = df_clusters['cluster'].nunique()
    cols = st.columns(num_clusters)
    
    for idx, cluster_id in enumerate(sorted(df_clusters['cluster'].unique())):
        with cols[idx]:
            cluster_data = df_clusters[df_clusters['cluster'] == cluster_id]
            st.markdown(f"""
            <div class="metric-card">
                <h3>Cluster {cluster_id}</h3>
                <p><strong>{len(cluster_data)}</strong> users</p>
                <p>Avg Spend: <strong>₹{cluster_data['total_spend'].mean():,.2f}</strong></p>
                <p>Avg Transactions: <strong>{cluster_data['transaction_count'].mean():.0f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Spending Distribution by Cluster")
        fig = px.box(
            df_clusters,
            x='cluster',
            y='total_spend',
            color='cluster',
            title="Spending Variation Across Clusters",
            labels={'cluster': 'Cluster', 'total_spend': 'Total Spending (₹)'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Cluster Size Distribution")
        cluster_counts = df_clusters['cluster'].value_counts().sort_index()
        fig = px.pie(
            values=cluster_counts.values,
            names=[f'Cluster {i}' for i in cluster_counts.index],
            title="User Distribution Across Clusters",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D scatter plot
    st.subheader("🎯 3D Cluster Visualization")
    fig = px.scatter_3d(
        df_clusters,
        x='total_spend',
        y='avg_spend',
        z='transaction_count',
        color='cluster',
        title="3D Cluster Representation",
        labels={
            'total_spend': 'Total Spending',
            'avg_spend': 'Avg Transaction',
            'transaction_count': 'Transaction Count'
        },
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_traces(marker=dict(size=5))
    st.plotly_chart(fig, use_container_width=True)
    
    # Category preferences by cluster
    st.subheader("🏷️ Category Preferences by Cluster")
    category_cols = [col for col in df_clusters.columns if col not in ['User_ID', 'total_spend', 'avg_spend', 'transaction_count', 'cluster']]
    cluster_categories = df_clusters.groupby('cluster')[category_cols].mean()
    
    fig = px.imshow(
        cluster_categories.T,
        labels=dict(x="Cluster", y="Category", color="Proportion"),
        x=[f'Cluster {i}' for i in cluster_categories.index],
        y=cluster_categories.columns,
        color_continuous_scale='YlOrRd',
        title="Category Spending Patterns by Cluster"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 5: RISK DETECTION
# ============================================================================
elif page == "⚠️ Risk Detection":
    st.title("⚠️ Risk Detection & Anomaly Analysis")
    
    # Calculate risk metrics
    df_features['spending_percentile'] = df_features['total_spend'].rank(pct=True)
    df_features['risk_score'] = (
        df_features['spending_percentile'] * 0.6 +
        (df_features['avg_spend'] / df_features['avg_spend'].max()) * 0.4
    )
    df_features['risk_level'] = pd.cut(
        df_features['risk_score'],
        bins=[0, 0.33, 0.66, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    # Risk overview
    col1, col2, col3 = st.columns(3)
    
    high_risk = (df_features['risk_level'] == 'High').sum()
    medium_risk = (df_features['risk_level'] == 'Medium').sum()
    low_risk = (df_features['risk_level'] == 'Low').sum()
    total_users = len(df_features)
    
    with col1:
        st.metric(
            label="🔴 High Risk Users",
            value=str(high_risk),
            delta=f"{high_risk/total_users*100:.1f}%"
        )
    
    with col2:
        st.metric(
            label="🟡 Medium Risk Users",
            value=str(medium_risk),
            delta=f"{medium_risk/total_users*100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="🟢 Low Risk Users",
            value=str(low_risk),
            delta=f"{low_risk/total_users*100:.1f}%"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Risk Distribution")
        risk_counts = df_features['risk_level'].value_counts()
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="User Risk Level Distribution",
            color=risk_counts.index,
            color_discrete_map={'Low': '#2ecc71', 'Medium': '#f39c12', 'High': '#e74c3c'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Spending vs Risk Score")
        fig = px.scatter(
            df_features,
            x='total_spend',
            y='risk_score',
            color='risk_level',
            size='avg_spend',
            title="Risk Score Analysis",
            labels={'total_spend': 'Total Spending (₹)', 'risk_score': 'Risk Score'},
            color_discrete_map={'Low': '#2ecc71', 'Medium': '#f39c12', 'High': '#e74c3c'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # High risk users table
    st.subheader("🚨 High Risk Users")
    high_risk_users = df_features[df_features['risk_level'] == 'High'].sort_values('risk_score', ascending=False)
    
    if len(high_risk_users) > 0:
        display_cols = ['User_ID', 'total_spend', 'avg_spend', 'transaction_count', 'risk_score']
        st.dataframe(
            high_risk_users[display_cols].head(10).style.background_gradient(subset=['risk_score'], cmap='Reds'),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No high-risk users detected!")
    
    # Anomaly detection on transactions
    st.subheader("🔍 Transaction Anomalies")
    
    # Calculate z-scores for amounts
    df_transactions['amount_zscore'] = (
        df_transactions['Amount'] - df_transactions['Amount'].mean()
    ) / df_transactions['Amount'].std()
    
    anomalies = df_transactions[abs(df_transactions['amount_zscore']) > 2.5].sort_values('amount_zscore', ascending=False)
    
    if len(anomalies) > 0:
        st.warning(f"Found {len(anomalies)} anomalous transactions (>2.5 std deviations)")
        st.dataframe(
            anomalies[['User_ID', 'Date', 'Amount', 'Category', 'Merchant', 'amount_zscore']].head(15),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No significant transaction anomalies detected!")

# ============================================================================
# PAGE 6: TRANSACTION EXPLORER
# ============================================================================
elif page == "🔍 Transaction Explorer":
    st.title("🔍 Transaction Explorer")
    
    # Filters
    st.sidebar.markdown("### 🔧 Filters")
    
    # Date range
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(df_transactions['Date'].min(), df_transactions['Date'].max()),
        min_value=df_transactions['Date'].min(),
        max_value=df_transactions['Date'].max()
    )
    
    # Category filter
    categories = st.sidebar.multiselect(
        "Categories",
        options=df_transactions['Category'].unique(),
        default=df_transactions['Category'].unique()
    )
    
    # Amount range
    amount_range = st.sidebar.slider(
        "Amount Range (₹)",
        min_value=float(df_transactions['Amount'].min()),
        max_value=float(df_transactions['Amount'].max()),
        value=(float(df_transactions['Amount'].min()), float(df_transactions['Amount'].max()))
    )
    
    # Apply filters
    filtered_df = df_transactions[
        (df_transactions['Date'] >= pd.to_datetime(date_range[0])) &
        (df_transactions['Date'] <= pd.to_datetime(date_range[1])) &
        (df_transactions['Category'].isin(categories)) &
        (df_transactions['Amount'] >= amount_range[0]) &
        (df_transactions['Amount'] <= amount_range[1])
    ]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    filtered_count = len(filtered_df)
    filtered_sum = filtered_df['Amount'].sum()
    filtered_mean = filtered_df['Amount'].mean()
    filtered_users = filtered_df['User_ID'].nunique()
    
    with col1:
        st.metric(
            label="Transactions",
            value=f"{filtered_count:,}"
        )
    
    with col2:
        st.metric(
            label="Total Amount",
            value=f"₹{filtered_sum:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Average",
            value=f"₹{filtered_mean:.2f}"
        )
    
    with col4:
        st.metric(
            label="Unique Users",
            value=f"{filtered_users}"
        )
    
    st.markdown("---")
    
    # Search
    search_term = st.text_input("🔎 Search Merchant", "")
    if search_term:
        filtered_df = filtered_df[filtered_df['Merchant'].str.contains(search_term, case=False, na=False)]
    
    # Display transactions
    st.subheader("📋 Transaction Details")
    st.dataframe(
        filtered_df.sort_values('Date', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Student Finance Intelligence**")
st.sidebar.markdown("Built with Streamlit & Plotly")
