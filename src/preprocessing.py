# handle missing values 
# remove duplicates 
# convert data -- datetime
# normalize amounts
# enncode categories

# input : raw data
# output: data/processed/cleanned.csv
# ---------------------------------------------------------------- 

import pandas as pd
INPUT_PATH = r"c:\Users\LENOVO\OneDrive\Desktop\DMW project\data\raw\student_personal_finance.csv"
OUTPUT_PATH = r"c:\Users\LENOVO\OneDrive\Desktop\DMW project\data\processed\cleaned.csv"

def load_data():
    df = pd.read_csv(INPUT_PATH)
    return df   

# correction 

def fix_types(df):
    df['Date'] = pd.to_datetime(df['Date'], errors="coerce")
    df['Amount'] = pd.to_numeric(df['Amount'], errors="coerce")
    return df

#      STANDARDZIING TEXT FIELDS :

def clean_text(df):
    df['Category'] = df['Category'].str.strip().str.lower()
    df['Payment_Type'] = df['Payment_Type'].str.strip().str.lower()
    df['Merchant'] = df['Merchant'].str.strip().str.lower()
    return df

#       REMOVE INAVLID ROWS : 

def remove_invalid_rows(df):
    df = df.dropna(subset=['Date', 'Amount'])
    df = df[df['Amount'] > 0]
    return df 

# Feature Engineering

def add_time_features(df):
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['weekday'] = df['Date'].dt.weekday
    return df


# SAVED CLEANED DATA

def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to {OUTPUT_PATH}")

#       MAIN PIPELINE 

def main():
    df = load_data()
    df = fix_types(df)
    df = clean_text(df)
    df = remove_invalid_rows(df)
    df = add_time_features(df)
    save_data(df)

if __name__ == "__main__":
    main()


