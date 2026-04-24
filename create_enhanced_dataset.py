import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_enhanced_dataset():
    """Create enhanced dataset with realistic timestamps and anomalies"""
    
    # Load original data
    df = pd.read_csv('data/raw/comprehensive_student_finance.csv')
    
    # Define realistic time patterns for different categories
    time_patterns = {
        'Rent': {'hour_range': (9, 17), 'weekday_preference': [0, 1, 2, 3, 4]},  # Business hours, weekdays
        'Food & Dining': {
            'breakfast': (7, 10), 'lunch': (11, 14), 'dinner': (18, 22),
            'late_night': (22, 2)
        },
        'Transportation': {'hour_range': (6, 23), 'peak_hours': [(7, 9), (16, 18)]},
        'Entertainment': {'hour_range': (18, 23), 'weekend_preference': [5, 6]},
        'Academic Supplies': {'hour_range': (9, 17), 'weekday_preference': [0, 1, 2, 3, 4]},
        'Clothing': {'hour_range': (10, 21), 'weekend_preference': [5, 6]},
        'Health': {'hour_range': (8, 18), 'weekday_preference': [0, 1, 2, 3, 4]},
        'Personal Care': {'hour_range': (9, 21)},
        'Utilities': {'hour_range': (9, 17), 'weekday_preference': [0, 1, 2, 3, 4]}
    }
    
    enhanced_data = []
    
    for idx, row in df.iterrows():
        date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
        category = row['Category']
        
        # Generate realistic timestamp based on category
        if category == 'Rent':
            # Rent payments during business hours
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            
        elif category == 'Food & Dining':
            # Meal times with some randomness
            meal_times = [
                random.randint(7, 10),    # Breakfast
                random.randint(11, 14),   # Lunch  
                random.randint(18, 22)    # Dinner
            ]
            hour = random.choice(meal_times)
            minute = random.randint(0, 59)
            
        elif category == 'Transportation':
            # Peak commute times or regular travel
            if random.random() < 0.4:  # 40% chance of peak time
                hour = random.choice([7, 8, 9, 16, 17, 18])
            else:
                hour = random.randint(6, 23)
            minute = random.randint(0, 59)
            
        elif category == 'Entertainment':
            # Evening and weekend entertainment
            if date_obj.weekday() >= 5:  # Weekend
                hour = random.randint(18, 23)
            else:  # Weekday
                hour = random.randint(19, 22)
            minute = random.randint(0, 59)
            
        elif category in ['Academic Supplies', 'Utilities', 'Health']:
            # Business hours on weekdays
            if date_obj.weekday() < 5:  # Weekday
                hour = random.randint(9, 17)
            else:  # Weekend - less likely but possible
                hour = random.randint(10, 16)
            minute = random.choice([0, 15, 30, 45])
            
        else:  # Personal Care, Clothing
            # Shopping hours
            hour = random.randint(10, 21)
            minute = random.randint(0, 59)
        
        # Create datetime with realistic timestamp
        timestamp = date_obj.replace(hour=hour, minute=minute, second=random.randint(0, 59))
        
        enhanced_data.append({
            'User_ID': row['User_ID'],
            'Date': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Amount': row['Amount'],
            'Category': row['Category'],
            'Payment_Type': row['Payment_Type'],
            'Merchant': row['Merchant']
        })
    
    # Create DataFrame with enhanced data
    enhanced_df = pd.DataFrame(enhanced_data)
    
    # Add some specific anomalies for detection
    anomalies = [
        # Late night large transactions (suspicious)
        {'User_ID': 'STU_2024_001', 'Date': '2024-01-15 02:30:00', 'Amount': 1500.00, 
         'Category': 'Rent', 'Payment_Type': 'Credit Card', 'Merchant': 'Luxury Apartment'},
        {'User_ID': 'STU_2024_002', 'Date': '2024-01-10 03:45:00', 'Amount': 65.90, 
         'Category': 'Food & Dining', 'Payment_Type': 'Credit Card', 'Merchant': 'Restaurant'},
        {'User_ID': 'STU_2024_003', 'Date': '2024-01-20 01:15:00', 'Amount': 300.00, 
         'Category': 'Clothing', 'Payment_Type': 'Digital Wallet', 'Merchant': 'Personal Trainer'},
        
        # Very early morning transactions
        {'User_ID': 'STU_2024_001', 'Date': '2024-01-08 05:00:00', 'Amount': 149.99, 
         'Category': 'Entertainment', 'Payment_Type': 'Digital Wallet', 'Merchant': 'Gaming Console'},
        {'User_ID': 'STU_2024_002', 'Date': '2024-01-14 04:30:00', 'Amount': 125.50, 
         'Category': 'Food & Dining', 'Payment_Type': 'Credit Card', 'Merchant': 'Gourmet Store'},
        
        # Unusual large amounts for category
        {'User_ID': 'STU_2024_003', 'Date': '2024-01-17 20:30:00', 'Amount': 450.00, 
         'Category': 'Clothing', 'Payment_Type': 'Credit Card', 'Merchant': 'Designer Store'},
        {'User_ID': 'STU_2024_001', 'Date': '2024-01-25 19:00:00', 'Amount': 95.40, 
         'Category': 'Food & Dining', 'Payment_Type': 'Digital Wallet', 'Merchant': 'Food Delivery'},
        
        # Multiple transactions in short time (potential fraud)
        {'User_ID': 'STU_2024_002', 'Date': '2024-01-12 14:00:00', 'Amount': 25.00, 
         'Category': 'Entertainment', 'Payment_Type': 'Credit Card', 'Merchant': 'Movie Theater'},
        {'User_ID': 'STU_2024_002', 'Date': '2024-01-12 14:05:00', 'Amount': 45.00, 
         'Category': 'Food & Dining', 'Payment_Type': 'Credit Card', 'Merchant': 'Restaurant'},
        {'User_ID': 'STU_2024_002', 'Date': '2024-01-12 14:10:00', 'Amount': 85.00, 
         'Category': 'Clothing', 'Payment_Type': 'Credit Card', 'Merchant': 'Fashion Store'},
    ]
    
    # Add anomalies to the dataset
    for anomaly in anomalies:
        enhanced_df = pd.concat([enhanced_df, pd.DataFrame([anomaly])], ignore_index=True)
    
    # Sort by date
    enhanced_df = enhanced_df.sort_values('Date').reset_index(drop=True)
    
    # Save enhanced dataset
    enhanced_df.to_csv('data/raw/comprehensive_student_finance_enhanced.csv', index=False)
    
    print(f"✅ Enhanced dataset created with {len(enhanced_df)} transactions")
    print(f"📊 Original: {len(df)} transactions")
    print(f"🔍 Added: {len(anomalies)} anomaly transactions")
    print(f"💾 Saved to: data/raw/comprehensive_student_finance_enhanced.csv")
    
    # Show sample of enhanced data
    print("\n📋 Sample of enhanced data:")
    print(enhanced_df.head(10))
    
    return enhanced_df

if __name__ == "__main__":
    create_enhanced_dataset()
