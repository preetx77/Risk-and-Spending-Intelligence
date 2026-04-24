# PREET SONAR 
# PRN : 20240802258

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the processed features data
INPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/features.csv"
df = pd.read_csv(INPUT_PATH)

print("🎯 CLASSIFICATION MODEL FOR OVERSPENDING RISK")
print("="*50)
print(f"Dataset shape: {df.shape}")
print(f"Users: {df['User_ID'].tolist()}")

# Create target variable (who overspends?)
# Using 75th percentile as threshold - above this = overspender (1), below = normal (0)
threshold = df['total_spend'].quantile(0.75)
df['overspend'] = (df['total_spend'] > threshold).astype(int)

print(f"\n📊 Target Variable:")
print(f"Overspend threshold: ₹{threshold:.2f}")
print(f"Class distribution:")
print(df['overspend'].value_counts().to_dict())

# Prepare features (X) and target (y)
# Remove User_ID (identifier) and overspend (target) from features
X = df.drop(columns=['User_ID', 'overspend'])
y = df['overspend']

print(f"\n🔧 Features prepared: {list(X.columns)}")

# Split data into training and testing sets
# 40% for testing, 60% for training
# Note: Cannot use stratify because we have too few samples (only 1 overspender)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)

print(f"\n📂 Data Split:")
print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Train Random Forest Classifier
# Random Forest = multiple decision trees voting together
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

print(f"\n✅ Model trained successfully!")

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate basic metrics
accuracy = accuracy_score(y_test, y_pred)

print(f"\n📊 MODEL PERFORMANCE:")
print(f"Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")

# Show detailed classification report
print(f"\n📋 Detailed Report:")
# Handle case where test set might only have one class
if len(np.unique(y_test)) == 2:
    print(classification_report(y_test, y_pred, target_names=['Normal Spender', 'Overspender']))
else:
    print("Test set contains only one class - cannot show full classification report")
    print(f"Actual test labels: {y_test.tolist()}")
    print(f"Predicted labels: {y_pred.tolist()}")

# Show which users were predicted correctly
print(f"\n👥 Individual Predictions:")
test_users = df.iloc[y_test.index]['User_ID'].values
test_actual = y_test.values
test_predicted = y_pred

for i, (user, actual, predicted) in enumerate(zip(test_users, test_actual, test_predicted)):
    actual_label = "Overspender" if actual == 1 else "Normal"
    predicted_label = "Overspender" if predicted == 1 else "Normal"
    status = "✅" if actual == predicted else "❌"
    print(f"{status} {user}: Actual={actual_label}, Predicted={predicted_label}")

# Feature importance - which features matter most?
print(f"\n🔍 FEATURE IMPORTANCE:")
importances = model.feature_importances_
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': importances
}).sort_values('importance', ascending=False)

# Show top 5 most important features
print("Top 5 predictors of overspending:")
for i, row in feature_importance.head(5).iterrows():
    print(f"{i+1}. {row['feature']}: {row['importance']:.3f}")

# Create simple bar chart of feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'])
plt.title('Feature Importance for Overspending Prediction')
plt.xlabel('Importance')
plt.tight_layout()
plt.show()

print(f"\n🎉 Classification analysis complete!")
print(f"💡 Key insight: {feature_importance.iloc[0]['feature']} is the strongest predictor of overspending")

