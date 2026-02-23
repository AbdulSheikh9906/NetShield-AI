import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("ids_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

st.title("🚀 Intrusion Detection System (ML Based)")

uploaded_file = st.file_uploader("Upload Network CSV File", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("Uploaded Data Preview:")
    st.write(data.head())

    # Ensure label column not present
    if "Label" in data.columns:
        data = data.drop("Label", axis=1)

    predictions = model.predict(data)

    decoded = label_encoder.inverse_transform(predictions)

    data["Prediction"] = decoded

    st.write("Prediction Results:")
    st.write(data.head())

    st.success("Prediction Completed!")