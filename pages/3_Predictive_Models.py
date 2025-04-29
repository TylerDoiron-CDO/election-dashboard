# pages/3_Predictive_Models.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, r2_score

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('data/Election_Data.csv', encoding='latin1')
    df.columns = df.columns.str.strip()

    # Parse dates
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
    df['Date'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')

    df = df.dropna(subset=['Year', 'Province_Territory', 'Election_Type', 'Parliament', 'Constituency', 'Votes'])
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data()

# -------------------------------
# Page Configuration
# -------------------------------
st.title("🔮 Predictive Models")
st.caption("Training predictive models to forecast election outcomes for 2025 based on historical data.")

# -------------------------------
# Data Preparation
# -------------------------------

# Define target
df['Win'] = df['Result'].str.contains('Elected', case=False, na=False).astype(int)

# Select features
features = ['Province_Territory', 'Political_Affiliation', 'Gender', 'Occupation']
df = df.dropna(subset=features)

# Encode Categorical Variables
encoder = LabelEncoder()
for col in features:
    df[col] = encoder.fit_transform(df[col].astype(str))

# Prepare data
X = df[['Year'] + features]
y_class = df['Win']
y_reg = df['Votes']

# Train on data before 2025
X_train = X[X['Year'] < 2025]
X_test = X[X['Year'] == 2025]
y_train_class = y_class[X['Year'] < 2025]
y_test_class = y_class[X['Year'] == 2025]
y_train_reg = y_reg[X['Year'] < 2025]
y_test_reg = y_reg[X['Year'] == 2025]

# -------------------------------
# Logistic Regression Model
# -------------------------------
st.header("📈 Logistic Regression: Predict Win vs Loss")

if not X_test.empty and not X_train.empty:
    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X_train, y_train_class)
    y_pred_class = log_model.predict(X_test)

    accuracy = accuracy_score(y_test_class, y_pred_class)

    st.metric(label="Accuracy on 2025 Data", value=f"{accuracy:.2%}")

    st.subheader("Classification Report")
    st.text(classification_report(y_test_class, y_pred_class, zero_division=0))

elif X_train.empty:
    st.warning("🚨 Not enough training data after applying filters. Please broaden your filters.")
else:
    # No 2025 test data — fallback to last available year
    last_year = X['Year'].max()
    st.warning(f"⚠️ No 2025 data available after filtering. Predicting for {last_year} instead.")
    
    X_fallback = X[X['Year'] == last_year]
    y_fallback = y_class[X['Year'] == last_year]
    
    y_pred_class = log_model.predict(X_fallback)
    accuracy = accuracy_score(y_fallback, y_pred_class)

    st.metric(label=f"Accuracy on {last_year} Data", value=f"{accuracy:.2%}")

    st.subheader("Classification Report")
    st.text(classification_report(y_fallback, y_pred_class, zero_division=0))

# -------------------------------
# Random Forest Model
# -------------------------------
st.header("🌳 Random Forest: Predict Vote Share")

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train_reg)
y_pred_reg = rf_model.predict(X_test)

r2 = r2_score(y_test_reg, y_pred_reg)
st.metric(label="R² Score on 2025 Data", value=f"{r2:.2f}")

# Feature Importances
importance = pd.DataFrame({'Feature': X_train.columns, 'Importance': rf_model.feature_importances_})
fig_importance = px.bar(
    importance.sort_values('Importance', ascending=True),
    x='Importance', y='Feature',
    orientation='h',
    title="Feature Importance (Random Forest)"
)
st.plotly_chart(fig_importance, use_container_width=True)

# -------------------------------
# Predicted vs Actual for 2025
# -------------------------------
st.header("🔍 Predicted vs Actual Results (2025)")

comparison = pd.DataFrame({
    'Actual Win': y_test_class.values,
    'Predicted Win': y_pred_class,
    'Actual Votes': y_test_reg.values,
    'Predicted Votes': y_pred_reg
})

st.dataframe(comparison, use_container_width=True)

# -------------------------------
# 🚀 Future Enhancements
# -------------------------------
st.header("🚀 Coming Soon: Advanced Predictive Models")

st.info(
    "- XGBoost Classification and Regression\n"
    "- ARIMA Time-Series Forecasting\n"
    "- Integration with Demographic and Geographic Datasets\n"
    "- More advanced machine learning pipelines"
)
