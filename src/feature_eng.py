# Monthly spend per user
# Category wise spend %
# Rolling averages
# Transaction frequency
# Avg spend per day
# Output: feature matrix

import pandas as pd

INPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/cleaned.csv"
OUTPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/features.csv"


def load_data():
    return pd.read_csv(INPUT_PATH)


# Aggregating user behaviours
def user_aggregation(df):
    user_df = df.groupby('User_ID').agg({
        'Amount': ['sum', 'mean', 'count']
    }).reset_index()

    user_df.columns = ['User_ID', 'total_spend', 'avg_spend', 'transaction_count']
    return user_df


# Category wise spending ratio
def category_features(df):
    cat_df = df.pivot_table(
        index='User_ID',
        columns='Category',
        values='Amount',
        aggfunc='sum',
        fill_value=0
    )
    # Convert to ratio
    cat_df = cat_df.div(cat_df.sum(axis=1), axis=0)
    cat_df = cat_df.reset_index()
    return cat_df


# Merge all features
def merge_features(user_df, cat_df):
    return pd.merge(user_df, cat_df, on='User_ID')


# Save
def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✓ Features saved: {df.shape} users, {df.shape} features")


def main():
    df = load_data()
    print(f"✓ Loaded {df.shape} transactions")
    
    user_df = user_aggregation(df)
    print(f"✓ Aggregated {user_df.shape} users")
    
    cat_df = category_features(df)
    print(f"✓ Generated category features")
    
    feature_df = merge_features(user_df, cat_df)
    print(f"✓ Merged features: {feature_df.shape}")
    
    save_data(feature_df)


if __name__ == "__main__":
    main()