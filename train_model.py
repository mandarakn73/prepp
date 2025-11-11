import os
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_FILE_CSV = "CET-CUTOFF2025.csv"
DATA_FILE_XLSX = "CET-CUTOFF2025.xlsx"
MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "ext_model.joblib")
ENC_FILE = os.path.join(MODEL_DIR, "label_encoder.joblib")

os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 60)
print("PREPPREDICT - EXTRA TREES MODEL TRAINING")
print("=" * 60)

# Load dataset
if os.path.exists(DATA_FILE_CSV):
    print(f"\n✓ Loading CSV dataset: {DATA_FILE_CSV}")
    df = pd.read_csv(DATA_FILE_CSV)
elif os.path.exists(DATA_FILE_XLSX):
    print(f"\n✓ Loading Excel dataset: {DATA_FILE_XLSX}")
    df = pd.read_excel(DATA_FILE_XLSX)
else:
    raise FileNotFoundError("No dataset found. Add CET-CUTOFF2025.csv or CET-CUTOFF2025.xlsx")

print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"\nColumns: {df.columns.tolist()}")

# Basic validation
required_cols = ['College', 'Branch']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Encode college names (target variable)
print("\n" + "=" * 60)
print("ENCODING TARGET VARIABLE")
print("=" * 60)

label_encoder = LabelEncoder()
df['College_encoded'] = label_encoder.fit_transform(df['College'])
print(f"✓ Encoded {len(label_encoder.classes_)} unique colleges")

# Select feature columns (caste cutoff ranks)
print("\n" + "=" * 60)
print("SELECTING FEATURES")
print("=" * 60)

# Common caste categories in Karnataka
caste_categories = [
    "GM", "1G", "1K", "1R",
    "2AG", "2AK", "2AR",
    "2BG", "2BK", "2BR",
    "3AG", "3AK", "3AR",
    "3BG", "3BK", "3BR",
    "GMK", "GMR",
    "SCG", "SCK", "SCR",
    "STG", "STK", "STR"
]

feature_cols = [col for col in caste_categories if col in df.columns]

if not feature_cols:
    print("⚠ No standard caste columns found. Using all numeric columns...")
    feature_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    feature_cols = [col for col in feature_cols if col != 'College_encoded']

print(f"✓ Selected {len(feature_cols)} features:")
for i, col in enumerate(feature_cols, 1):
    print(f"  {i}. {col}")

# Prepare data
X = df[feature_cols].fillna(0)
y = df['College_encoded']

print(f"\n✓ Feature matrix shape: {X.shape}")
print(f"✓ Target vector shape: {y.shape}")

# Train-test split
print("\n" + "=" * 60)
print("SPLITTING DATA")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Training set: {X_train.shape[0]} samples")
print(f"✓ Testing set: {X_test.shape[0]} samples")

# Train Extra Trees model
print("\n" + "=" * 60)
print("TRAINING EXTRA TREES CLASSIFIER")
print("=" * 60)

model = ExtraTreesClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

print("\nTraining model...")
model.fit(X_train, y_train)

# Evaluate
print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✓ Accuracy: {accuracy:.2%}")
print(f"✓ Training samples: {len(X_train)}")
print(f"✓ Testing samples: {len(X_test)}")

# Feature importance
print("\n" + "=" * 60)
print("TOP 5 FEATURE IMPORTANCES")
print("=" * 60)

feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(5).iterrows():
    print(f"  {row['feature']}: {row['importance']:.4f}")

# Save model
print("\n" + "=" * 60)
print("SAVING MODEL")
print("=" * 60)

joblib.dump(model, MODEL_FILE)
joblib.dump(label_encoder, ENC_FILE)
joblib.dump(feature_cols, os.path.join(MODEL_DIR, "feature_cols.joblib"))

print(f"✓ Model saved to: {MODEL_FILE}")
print(f"✓ Encoder saved to: {ENC_FILE}")
print(f"✓ Feature columns saved")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print(f"\n✅ Model accuracy: {accuracy:.2%}")
print(f"✅ Ready for deployment\n")
