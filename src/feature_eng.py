# monntly spend per use
# category wise spend %
# rolling averages
# transaction frequency
# avg spend per day

# output : feature matrix

import pandas as pd

INPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/ingested.csv"
OUTPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/features.csv"

def load_data():
    return pd.read_csv(INPUT_PATH)

    # aggregating user behaviours 

def user_aggregation(df):
    user_df = df.groupby('user_id').agg({
        'amount': ['sum', 'mean', 'count']
    }).reset_index()

    user_df.columns = ['user_id', 'total_spend', 'avg_spend', 'transaction_count']
    return user_df

#     Category wise spennding ratio

def category_features(df):
    cat_df = df.pivot_table(
        index = 'user_id',
        columns = 'category',
        values = 'amount',
        aggfunc = 'sum',
        fill_value = 0
    )
     #convert to ratio
    cat_df = cat_df.div(cat_df.sum(axis=1), axis=0)
    cat_df = cat_df.reset_index()

    return cat_df

    # Merge all features
    
def merge_features(user_df, cat_df):
    return pd.merge(user_df, cat_df, on = 'user_id')

    # SAVE

def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print("Data saved!")

def main():
    df = load_data()
    user_df = user_aggregation(df)
    cat_df = category_features(df)
    feature_df = merge_features(user_df, cat_df)
    save_data(feature_df)

if __name__ == "__main__":
    main()