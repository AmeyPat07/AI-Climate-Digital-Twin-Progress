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


# --------------------------------------------------
# Project modules
# --------------------------------------------------

from src.forecasting import (
    simulate_anomaly_scenario
)

from src.digital_twin import (
    create_digital_twin_state
)

from src.climate_state import (
    build_climate_state
)

from src.environment import (
    get_environment_state
)

from src.environment_ui import (
    render_environment
)

from src.weather import (
    create_weather_state
)


# --------------------------------------------------
# Model and data paths
# --------------------------------------------------

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
# Load model
# --------------------------------------------------

model = joblib.load(
    MODEL_PATH
)


# --------------------------------------------------
# Load monthly climatology
# --------------------------------------------------

monthly_climatology = pd.read_csv(
    CLIMATOLOGY_PATH,
    index_col=0
).squeeze(
    "columns"
)

monthly_climatology.index = (
    monthly_climatology.index.astype(int)
)


# --------------------------------------------------
# Load operational forecast data
# --------------------------------------------------

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
    page_title=(
        "Maharashtra Climate Digital Twin"
    ),
    page_icon="🌡️",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

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


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header(
    "Historical Climate State"
)

st.sidebar.divider()

st.sidebar.header(
    "Atmospheric Scenario"
)


# --------------------------------------------------
# Weather scenario selection
# --------------------------------------------------

weather_condition = st.sidebar.selectbox(
    "Weather condition",
    options=[
        "clear",
        "partly_cloudy",
        "cloudy",
        "rain",
        "storm",
        "fog"
    ],
    index=2,
    format_func=lambda value: {
        "clear": "☀️ Clear",
        "partly_cloudy": "🌤️ Partly Cloudy",
        "cloudy": "☁️ Cloudy",
        "rain": "🌧️ Rain",
        "storm": "⛈️ Storm",
        "fog": "🌫️ Fog"
    }[value]
)


weather_state = create_weather_state(
    weather_condition
)


# --------------------------------------------------
# Historical date selection
# --------------------------------------------------

available_dates = (
    forecast_data.index.sort_values()
)

selected_date = st.sidebar.date_input(
    "Reference date",
    value=available_dates[0].date(),
    min_value=available_dates[0].date(),
    max_value=available_dates[-1].date()
)

selected_date = pd.Timestamp(
    selected_date
)


# ==================================================
# CURRENT CLIMATE STATE
# ==================================================

row = forecast_data.loc[
    selected_date
]


# --------------------------------------------------
# Current anomaly
# --------------------------------------------------

today_anomaly = float(
    row["actual_anomaly_C"]
)


# --------------------------------------------------
# Forecast date
# --------------------------------------------------

forecast_date = pd.Timestamp(
    row["forecast_date"]
)


# --------------------------------------------------
# Previous-day anomaly
# --------------------------------------------------

yesterday_date = (
    selected_date
    - pd.Timedelta(days=1)
)


if yesterday_date in forecast_data.index:

    yesterday_anomaly = float(
        forecast_data.loc[
            yesterday_date,
            "actual_anomaly_C"
        ]
    )

else:

    yesterday_anomaly = (
        today_anomaly
    )


# --------------------------------------------------
# Monthly climatological baseline
# --------------------------------------------------

monthly_baseline = float(
    monthly_climatology.loc[
        selected_date.month
    ]
)


# --------------------------------------------------
# Current temperature
# --------------------------------------------------

current_temperature = (
    monthly_baseline
    + today_anomaly
)


# ==================================================
# CLIMATE STATE ENGINE
# ==================================================

current_climate_state = (
    build_climate_state(
        temperature_C=current_temperature,
        anomaly_C=today_anomaly,
        climatology_C=monthly_baseline,
        extreme_heat_risk=(
            today_anomaly >= 3
        )
    )
)


# ==================================================
# ENVIRONMENT STATE
# ==================================================

environment_state = (
    get_environment_state(
        current_climate_state.status,
        today_anomaly
    )
)


# ==================================================
# ATMOSPHERIC ENVIRONMENT
# ==================================================

render_environment(
    environment_state,
    weather_state
)


# ==================================================
# DIGITAL TWIN ENGINE
# ==================================================

digital_twin_state = (
    create_digital_twin_state(
        model=model,
        monthly_climatology=monthly_climatology,
        current_date=selected_date,
        forecast_date=forecast_date,
        current_anomaly_C=today_anomaly,
        previous_anomaly_C=yesterday_anomaly
    )
)


# ==================================================
# CURRENT STATE METRICS
# ==================================================

st.subheader(
    "Current Climate State"
)


col1, col2, col3, col4 = (
    st.columns(4)
)


col1.metric(
    "Current Temperature",
    (
        f"{digital_twin_state.current_temperature_C:.2f}"
        " °C"
    )
)


col2.metric(
    "Current Anomaly",
    (
        f"{digital_twin_state.current_anomaly_C:+.2f}"
        " °C"
    )
)


col3.metric(
    "Climatology",
    (
        f"{digital_twin_state.climatological_temperature_C:.2f}"
        " °C"
    )
)


col4.metric(
    "Status",
    current_climate_state.status
)


# ==================================================
# NEXT-DAY FORECAST
# ==================================================

st.subheader(
    "Next-Day Forecast"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Forecast Date",
    digital_twin_state.forecast_date.strftime(
        "%Y-%m-%d"
    )
)

col2.metric(
    "Predicted Temperature",
    (
        f"{digital_twin_state.predicted_temperature_C:.2f}"
        " °C"
    )
)

col3.metric(
    "Predicted Anomaly",
    (
        f"{digital_twin_state.predicted_anomaly_C:+.2f}"
        " °C"
    )
)


# ==================================================
# FORECAST UNCERTAINTY
# ==================================================

st.subheader(
    "Forecast Uncertainty"
)

st.caption(
    "Empirical 95% prediction interval derived "
    "from validation residuals."
)

uncertainty_col1, uncertainty_col2, uncertainty_col3 = (
    st.columns(3)
)

uncertainty_col1.metric(
    "Lower Bound",
    (
        f"{digital_twin_state.prediction_lower_C:+.2f}"
        " °C"
    )
)

uncertainty_col2.metric(
    "Expected Forecast",
    (
        f"{digital_twin_state.predicted_anomaly_C:+.2f}"
        " °C"
    )
)

uncertainty_col3.metric(
    "Upper Bound",
    (
        f"{digital_twin_state.prediction_upper_C:+.2f}"
        " °C"
    )
)


# --------------------------------------------------
# Temperature prediction range
# --------------------------------------------------

forecast_lower_temperature = (
    digital_twin_state.predicted_temperature_C
    + digital_twin_state.prediction_lower_C
    - digital_twin_state.predicted_anomaly_C
)

forecast_upper_temperature = (
    digital_twin_state.predicted_temperature_C
    + digital_twin_state.prediction_upper_C
    - digital_twin_state.predicted_anomaly_C
)


st.write(
    "**Expected temperature range:** "
    f"{forecast_lower_temperature:.2f} °C "
    "– "
    f"{forecast_upper_temperature:.2f} °C"
)

st.caption(
    "The interval is asymmetric because the validation "
    "residual distribution is asymmetric."
)


# ==================================================
# HEAT RISK ASSESSMENT
# ==================================================

st.divider()

st.subheader(
    "🔥 Heat Risk Assessment"
)


risk_col1, risk_col2 = st.columns(
    [1, 2]
)


with risk_col1:

    st.metric(
        "Heat Risk Score",
        (
            f"{digital_twin_state.heat_risk_score:.1f}"
            " / 100"
        )
    )

    st.metric(
        "Risk Category",
        digital_twin_state.heat_risk_category
    )


with risk_col2:

    st.write(
        "**Risk Components**"
    )

    st.write(
        "Current anomaly: "
        f"{digital_twin_state.anomaly_risk_component:.1f}"
        " / 60"
    )

    st.write(
        "Persistence: "
        f"{digital_twin_state.persistence_risk_component:.1f}"
        " / 25"
    )

    st.write(
        "Forecast severity: "
        f"{digital_twin_state.forecast_risk_component:.1f}"
        " / 15"
    )


# ==================================================
# RISK INTERPRETATION
# ==================================================

if (
    digital_twin_state.heat_risk_category
    == "Extreme"
):

    st.error(
        "⚠️ Extreme heat risk detected by the "
        "calibrated Digital Twin risk engine."
    )

elif (
    digital_twin_state.heat_risk_category
    == "High"
):

    st.warning(
        "High heat-risk conditions detected."
    )

elif (
    digital_twin_state.heat_risk_category
    == "Moderate"
):

    st.info(
        "Moderate heat-risk conditions detected."
    )

else:

    st.success(
        "✓ Low heat-risk conditions."
    )


st.caption(
    "Risk threshold calibrated on 729 validation "
    "forecast cases. Extreme-risk threshold: "
    f"{digital_twin_state.risk_threshold:.0f}/100."
)



# ==================================================
# TEMPERATURE UNCERTAINTY RANGE
# ==================================================

forecast_lower_temperature = (
    digital_twin_state.predicted_temperature_C
    + digital_twin_state.prediction_lower_C
    - digital_twin_state.predicted_anomaly_C
)

forecast_upper_temperature = (
    digital_twin_state.predicted_temperature_C
    + digital_twin_state.prediction_upper_C
    - digital_twin_state.predicted_anomaly_C
)


st.write(
    "**Expected temperature range:** "
    f"{forecast_lower_temperature:.2f} °C "
    "– "
    f"{forecast_upper_temperature:.2f} °C"
)


st.caption(
    "The interval is asymmetric because the validation "
    "residual distribution is asymmetric."
)


# ==================================================
# SCENARIO SIMULATION
# ==================================================

st.divider()

st.header(
    "Scenario Simulation"
)

st.write(
    "Change the current climate state and "
    "observe the modeled next-day response."
)


col1, col2 = (
    st.columns(2)
)


with col1:

    scenario_today = st.slider(
        "Today's anomaly (°C)",
        min_value=-5.0,
        max_value=6.0,
        value=float(
            today_anomaly
        ),
        step=0.1
    )


with col2:

    scenario_yesterday = st.slider(
        "Yesterday's anomaly (°C)",
        min_value=-5.0,
        max_value=6.0,
        value=float(
            yesterday_anomaly
        ),
        step=0.1
    )


# --------------------------------------------------
# Scenario forecast
# --------------------------------------------------

scenario = (
    simulate_anomaly_scenario(
        model=model,
        monthly_climatology=monthly_climatology,
        today_anomaly=scenario_today,
        yesterday_anomaly=scenario_yesterday,
        forecast_date=forecast_date
    )
)


# --------------------------------------------------
# Scenario metrics
# --------------------------------------------------

col1, col2, col3 = (
    st.columns(3)
)


col1.metric(
    "Scenario Prediction",
    (
        f"{scenario['predicted_anomaly_C']:+.2f}"
        " °C"
    )
)


col2.metric(
    "Scenario Temperature",
    (
        f"{scenario['predicted_temperature_C']:.2f}"
        " °C"
    )
)


col3.metric(
    "Scenario Heat Risk",
    (
        "YES"
        if scenario["extreme_heat_risk"]
        else "NO"
    )
)


# ==================================================
# HISTORICAL FORECAST COMPARISON
# ==================================================

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
        "forecast_date":
            "Forecast Date",

        "actual_anomaly_C":
            "Actual Anomaly (°C)",

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


# ==================================================
# MODEL INFORMATION
# ==================================================

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


# ==================================================
# MODEL VALIDATION
# ==================================================

st.divider()

st.header(
    "Model Validation"
)


st.caption(
    "Performance evaluated on unseen "
    "2023–2024 data."
)


col1, col2, col3, col4 = (
    st.columns(4)
)


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
    "**Extreme-heat detection recall:** "
    "47.62%"
)


st.write(
    "**Persistence baseline recall:** "
    "66.67%"
)