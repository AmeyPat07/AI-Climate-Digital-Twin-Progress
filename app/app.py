import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.forecasting import (
    digital_twin_forecast,
    simulate_anomaly_scenario
)


MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_linear_model.joblib"
)

CLIMATOLOGY_PATH = (
    PROJECT_ROOT
    / "models"
    / "monthly_climatology.csv"
)

FORECAST_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "operational_forecasts_2023_2024.csv"
)


# --------------------------------------------------
# Load model and climate data
# --------------------------------------------------

model = joblib.load(MODEL_PATH)

monthly_climatology = pd.read_csv(
    CLIMATOLOGY_PATH,
    index_col=0
).squeeze("columns")

monthly_climatology.index = (
    monthly_climatology.index.astype(int)
)


forecast_data = pd.read_csv(
    FORECAST_PATH,
    index_col=0,
    parse_dates=True
)

forecast_data.index.name = "date"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Maharashtra Climate Digital Twin",
    page_icon="🌡️",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(
    "🌡️ Maharashtra Climate Digital Twin"
)

st.caption(
    "Next-day temperature anomaly forecasting "
    "and extreme-heat risk assessment"
)
st.info(
    """
    **Digital Twin objective**

    This prototype represents the daily maximum-temperature
    state using historical climatology and temperature anomalies,
    forecasts the next day's anomaly using a validated temporal
    regression model, and provides an extreme-heat risk signal
    using a persistence-based detector.

    **Forecast model:** Minimal Linear Regression

    **Forecast inputs:** Current anomaly + one-day lag anomaly

    **Risk threshold:** Temperature anomaly ≥ +3°C
    """
)

# --------------------------------------------------
# Historical date selection
# --------------------------------------------------

st.sidebar.header(
    "Historical Climate State"
)

available_dates = forecast_data.index.sort_values()

selected_date = st.sidebar.date_input(
    "Reference date",
    value=available_dates[0].date(),
    min_value=available_dates[0].date(),
    max_value=available_dates[-1].date()
)

selected_date = pd.Timestamp(
    selected_date
)


# --------------------------------------------------
# Current state
# --------------------------------------------------

row = forecast_data.loc[selected_date]

today_anomaly = float(
    row["actual_anomaly_C"]
)

forecast_date = pd.Timestamp(
    row["forecast_date"]
)

yesterday_date = selected_date - pd.Timedelta(days=1)

if yesterday_date in forecast_data.index:

    yesterday_anomaly = float(
        forecast_data.loc[
            yesterday_date,
            "actual_anomaly_C"
        ]
    )

else:

    yesterday_anomaly = today_anomaly


monthly_baseline = float(
    monthly_climatology.loc[
        selected_date.month
    ]
)

current_temperature = (
    monthly_baseline
    + today_anomaly
)

current_status = (
    "Extreme heat"
    if today_anomaly >= 3
    else
    "Above normal"
    if today_anomaly > 1
    else
    "Below normal"
    if today_anomaly < -1
    else
    "Near normal"
)


# --------------------------------------------------
# Forecast
# --------------------------------------------------

forecast = digital_twin_forecast(
    model=model,
    monthly_climatology=monthly_climatology,
    today_anomaly=today_anomaly,
    yesterday_anomaly=yesterday_anomaly,
    forecast_date=forecast_date
)


# --------------------------------------------------
# Current state metrics
# --------------------------------------------------

st.subheader(
    "Current Climate State"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Temperature",
    f"{current_temperature:.2f} °C"
)

col2.metric(
    "Current Anomaly",
    f"{today_anomaly:+.2f} °C"
)

col3.metric(
    "Climatology",
    f"{monthly_baseline:.2f} °C"
)

col4.metric(
    "Status",
    current_status
)


# --------------------------------------------------
# Forecast metrics
# --------------------------------------------------

st.subheader(
    "Next-Day Forecast"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Forecast Date",
    forecast_date.strftime("%Y-%m-%d")
)

col2.metric(
    "Predicted Temperature",
    f"{forecast['predicted_temperature_C']:.2f} °C"
)

col3.metric(
    "Predicted Anomaly",
    f"{forecast['predicted_anomaly_C']:+.2f} °C"
)

risk = forecast["extreme_heat_risk"]

col4.metric(
    "Extreme Heat Risk",
    "YES" if risk else "NO"
)


# --------------------------------------------------
# Risk message
# --------------------------------------------------

if risk:

    st.error(
        "⚠️ Extreme heat risk detected."
    )

else:

    st.success(
        "✓ No extreme heat risk detected."
    )


# --------------------------------------------------
# Scenario simulator
# --------------------------------------------------

st.divider()

st.header(
    "Scenario Simulation"
)

st.write(
    "Change the current climate state and "
    "observe the modeled next-day response."
)

col1, col2 = st.columns(2)

with col1:

    scenario_today = st.slider(
        "Today's anomaly (°C)",
        min_value=-5.0,
        max_value=6.0,
        value=float(today_anomaly),
        step=0.1
    )

with col2:

    scenario_yesterday = st.slider(
        "Yesterday's anomaly (°C)",
        min_value=-5.0,
        max_value=6.0,
        value=float(yesterday_anomaly),
        step=0.1
    )


scenario = simulate_anomaly_scenario(
    model=model,
    monthly_climatology=monthly_climatology,
    today_anomaly=scenario_today,
    yesterday_anomaly=scenario_yesterday,
    forecast_date=forecast_date
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "Scenario Prediction",
    f"{scenario['predicted_anomaly_C']:+.2f} °C"
)

col2.metric(
    "Scenario Temperature",
    f"{scenario['predicted_temperature_C']:.2f} °C"
)

col3.metric(
    "Scenario Heat Risk",
    "YES"
    if scenario["extreme_heat_risk"]
    else "NO"
)


# --------------------------------------------------
# Historical forecast comparison
# --------------------------------------------------

st.divider()

st.header(
    "Historical Forecast"
)

comparison = forecast_data[
    [
        "forecast_date",
        "actual_anomaly_C",
        "predicted_anomaly_C"
    ]
].copy()

comparison = comparison.rename(
    columns={
        "forecast_date": "Forecast Date",
        "actual_anomaly_C": "Actual Anomaly (°C)",
        "predicted_anomaly_C":
            "Predicted Anomaly (°C)"
    }
)

comparison = comparison.set_index(
    "Forecast Date"
)

st.line_chart(
    comparison[
        [
            "Actual Anomaly (°C)",
            "Predicted Anomaly (°C)"
        ]
    ]
)


# --------------------------------------------------
# Model information
# --------------------------------------------------

st.divider()

st.subheader(
    "Forecasting Model"
)

st.write(
    "Minimal Linear Regression"
)

st.write(
    "Features: current anomaly and "
    "one-day lag anomaly."
)

st.write(
    "Validation MAE: 0.6143 °C"
)

st.write(
    "Validation RMSE: 0.8869 °C"
)

# --------------------------------------------------
# Model validation
# --------------------------------------------------

st.divider()

st.header(
    "Model Validation"
)

st.caption(
    "Performance evaluated on unseen 2023–2024 data."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Overall MAE",
    "0.6143 °C"
)

col2.metric(
    "Overall RMSE",
    "0.8869 °C"
)

col3.metric(
    "2023 MAE",
    "0.6352 °C"
)

col4.metric(
    "2024 MAE",
    "0.5935 °C"
)

st.write(
    "**Extreme-heat detection recall:** 47.62%"
)

st.write(
    "**Persistence baseline recall:** 66.67%"
)