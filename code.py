import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to estimate HbA1c based on average glucose level
def estimate_hba1c(avg_glucose):
    return (avg_glucose + 46.7) / 28.7

# Function to provide health advice
def health_advice(fasting, postprandial):
    if fasting < 70:
        return "Your fasting glucose is low. Consider consulting a doctor."
    elif 70 <= fasting <= 99 and postprandial < 140:
        return "Your glucose levels are normal. Maintain a healthy lifestyle!"
    elif 100 <= fasting <= 125 or 140 <= postprandial < 200:
        return "Your glucose levels indicate prediabetes. Consider lifestyle changes."
    else:
        return "Your glucose levels are high. Consult a healthcare provider."

# Streamlit layout
st.set_page_config(page_title="Blood Glucose & HbA1c Tracker", layout="wide")
st.title("🩸 Blood Glucose & HbA1c Tracker")

# User inputs
st.header("Enter Your Glucose Levels")
fasting_glucose = st.number_input("Fasting Blood Glucose (mg/dL)", min_value=0, step=1)
postprandial_glucose = st.number_input("Postprandial Blood Glucose (mg/dL)", min_value=0, step=1)

if st.button("Calculate HbA1c"):
    avg_glucose = (fasting_glucose + postprandial_glucose) / 2
    estimated_hba1c = estimate_hba1c(avg_glucose)
    advice = health_advice(fasting_glucose, postprandial_glucose)

    st.subheader("Results")
    st.write(f"**Estimated HbA1c**: {estimated_hba1c:.2f}%")
    st.write(f"**Health Advice**: {advice}")

    # Store data for plotting
    if "glucose_data" not in st.session_state:
        st.session_state.glucose_data = []
    st.session_state.glucose_data.append(
        {"Fasting": fasting_glucose, "Postprandial": postprandial_glucose, "HbA1c": estimated_hba1c}
    )

# Display trends if data exists
if "glucose_data" in st.session_state and st.session_state.glucose_data:
    st.header("📈 Glucose Level Trends")
    df = pd.DataFrame(st.session_state.glucose_data)
    
    # Plot fasting and postprandial glucose trends
    fig, ax = plt.subplots()
    df[['Fasting', 'Postprandial']].plot(kind='line', ax=ax, marker='o')
    ax.set_title("Glucose Levels Over Time")
    ax.set_xlabel("Entry")
    ax.set_ylabel("Glucose Level (mg/dL)")
    st.pyplot(fig)

    # Display data as a table
    st.write("### Recorded Data")
    st.dataframe(df)
