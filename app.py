# app.py
import streamlit as st
import pandas as pd
import joblib
import os
from utils import offline_summary

st.set_page_config(page_title="PrepPredict (Extra Trees)", layout="wide")

DATA_FILE = "CET-CUTOFF2025.xlsx"
MODEL_FILE = "models/ext_model.joblib"
ENC_FILE = "models/label_encoder.joblib"

st.title("PrepPredict — KCET College Predictor (Offline)")

# Load dataset
if not os.path.exists(DATA_FILE):
    st.error(f"Dataset file missing: {DATA_FILE}")
    st.stop()

df = pd.read_csv(DATA_FILE)

# Load model if available
model = None
label_encoder = None
if os.path.exists(MODEL_FILE) and os.path.exists(ENC_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        label_encoder = joblib.load(ENC_FILE)
        st.success("Loaded trained Extra Trees model.")
    except Exception as e:
        st.warning(f"Model could not be loaded: {e}")

# UI inputs
col1, col2 = st.columns(2)
with col1:
    rank = st.number_input("Enter KCET Rank", min_value=1, max_value=100000, value=5000, step=1)
with col2:
    caste_choices = [c for c in df.columns if c not in ["College","Branch","Location","CETCode","College_encoded"]]
    if not caste_choices:
        caste_choices = ["GM"]  # fallback
    caste = st.selectbox("Caste Code", options=caste_choices, index=0)

st.markdown("### Predictions")

# If model exists, predict using the Extra Trees model
if model is not None and label_encoder is not None:
    # Create a sample input: use rank as proxy for many cutoff columns (simple approach)
    feature_cols = [c for c in df.columns if c not in ["College","Branch","Location","CETCode","College_encoded"]]
    # Use 0 -> fillna; for basic demo use rank for each feature present
    X_sample = pd.DataFrame([[rank]*len(feature_cols)], columns=feature_cols)
    try:
        pred_enc = int(round(model.predict(X_sample)[0]))
        try:
            predicted_college = label_encoder.inverse_transform([pred_enc])[0]
        except Exception:
            predicted_college = "Prediction mapping failed"
        st.info(f"Extra Trees predicted college (approx): **{predicted_college}**")
    except Exception as e:
        st.warning(f"Model prediction failed: {e}")

# Also show top eligible colleges by filtering (original logic)
caste_col = caste
eligible = df[df.get(caste_col, 0) >= rank].copy()
if eligible.empty:
    st.warning("No colleges found using simple cutoff filtering for this rank & caste.")
else:
    eligible["ChanceScore"] = eligible.get(caste_col, 0) - rank
    eligible = eligible.sort_values(by="ChanceScore", ascending=False)
    top5 = eligible.head(5)
    st.write("Top colleges (based on cutoff & chance score):")
    st.dataframe(top5[["CETCode","College","Branch","Location", caste_col, "ChanceScore"]].reset_index(drop=True), height=300)

    st.markdown("### College Summaries")
    for _, row in top5.iterrows():
        summary, score = offline_summary(row, rank)
        st.markdown(f"**{row['College']}** ({row['Branch']}) — Score: {score}/10")
        st.text(summary)
        st.markdown("---")

st.caption("Model-based prediction uses a simple feature proxy (rank -> cutoff features). Improve by engineering features and re-training.")

