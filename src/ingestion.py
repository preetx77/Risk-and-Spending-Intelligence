# load dataset (CSV / API)
# standardized coloumns
# output : data/raw / transaction.csv
# ----------------------------------------------------------------------------------

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\DMW project\data\raw\student_personal_finance.csv"
OUTPUT_PATH = r"C:\Users\LENOVO\OneDrive\Desktop\DMW project\data\processed\ingested.csv"

def load_data():
    df = pd.read_csv(RAW_PATH)
    return df

def basic_inspection(df):
    print("Shape : ", df.shape)
    print("Columns : ", df.columns.tolist())
    print("Data Types : ", df.dtypes)
    print("Missing values : ", df.isnull().sum())
    print("sample : ", df.head())

    # standardzing columns

def standardize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df   

def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)

def main():
    df = load_data()
    basic_inspection(df)
    df = standardize_columns(df)
    save_data(df)

if __name__ == "__main__":
    main()




