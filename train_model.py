# train_model.py
import os
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
import joblib

# Paths
DATA_FILE = "CET-CUTOFF2025.csv"
MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "ext_model.joblib")
ENC_FILE = os.path.join(MODEL_DIR, "label_encoder.joblib")

os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Basic check
print("Columns in CSV:", df.columns.tolist())
# Ensure 'College' exists
if "College" not in df.columns:
    raise ValueError("CSV must contain a 'College' column. Update CSV or the script.")

# Encode the college label (target)
label_encoder = LabelEncoder()
df["College_encoded"] = label_encoder.fit_transform(df["College"])

# Select feature columns. Update these to match your CSV caste-cutoff columns
feature_cols = []
# Prefer columns that contain cutoff ranks, e.g. GM, 1G, 2AG, 3AG etc.
possible = ["GM","1G","1K","1R","2AG","2AK","2AR","2BG","2BK","2BR","3AG","3AK","3AR","3BG","3BK","3BR"]
for c in possible:
    if c in df.columns:
        feature_cols.append(c)

if not feature_cols:
    raise ValueError("No feature columns found. Update 'possible' list or CSV columns.")

print("Using features:", feature_cols)

X = df[feature_cols].fillna(0)
y = df["College_encoded"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Extra Trees
model = ExtraTreesRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
r2 = r2_score(y_test, model.predict(X_test))
print(f"Trained Extra Trees — R²: {r2:.3f}")

# Save model and encoder
joblib.dump(model, MODEL_FILE)
joblib.dump(label_encoder, ENC_FILE)
print(f"Saved model to {MODEL_FILE}")
print(f"Saved label encoder to {ENC_FILE}")
