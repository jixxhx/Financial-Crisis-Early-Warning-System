import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

print("Starting AI Model Training (Advanced Mode)...")

# 1. Load Data
df = pd.read_csv('financial_dataset.csv', index_col=0, parse_dates=True)

# 2. Define 'Crisis' (Target Variable)
# Definition: If the price drops by more than 5% within a month (20 trading days).
df['Return'] = df['S&P500'].pct_change(20) 
df['Target'] = (df['Return'] < -0.05).astype(int)

# 3. Create Features (Lagging)
# Using 'Lag' features to predict the future.
df['VIX_Lag'] = df['VIX'].shift(20)
df['Oil_Lag'] = df['Oil'].shift(20)
df['T10Y2Y_Lag'] = df['T10Y2Y'].shift(20)
df['Gold_Lag'] = df['Gold'].shift(20) # Gold Added

df = df.dropna()

# 4. Train/Test Split
features = ['VIX_Lag', 'Oil_Lag', 'T10Y2Y_Lag', 'Gold_Lag']
X = df[features]
y = df['Target']

# Split data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 5. Train Model with 'Balanced' Weight
# class_weight='balanced': Pays more attention to the minority class (Crisis)
model = RandomForestClassifier(n_estimators=200, max_depth=5, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate Performance
print(">> Model Training Completed.")
print("\n[AI Performance Report]")
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Feature Importance
importances = model.feature_importances_
print("\n[Feature Importance]")
for name, score in zip(features, importances):
    print(f"{name}: {score:.4f}")

print("\nSuccess! Advanced AI Model built successfully.")