import pandas as pd

INPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/features.csv"

df = pd.read_csv(INPUT_PATH)


# create target variables

threshold = df['total_spend'].quantile(0.75)
df['overspend'] = (df['total_spend'] > threshold).astype(int)

# prepare features

X = df.drop(columns = ['User_ID' , 'overspend'])
y = df['overspend']

# train test split

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size = 0.4, random_state = 42
)

# train model 

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state = 42)
model.fit(X_train, y_train)

# evaluate model

from sklearn.metrics import accuracy_score, classification_report

y_pred = model.predict(X_test)

print("Accuracy : ", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# feature importance

import matplotlib.pyplot as plt

importances = model.feature_importances_

plt.barh(X.columns, importances)
plt.title("Feature Importance")
plt.show()

