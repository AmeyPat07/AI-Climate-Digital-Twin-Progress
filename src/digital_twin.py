from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.risk import (
    calculate_heat_risk,
    load_heat_risk_calibration
)


@dataclass
class DigitalTwinState:
    """
    Complete computational state of the climate Digital Twin.

    Contains:

    - Current climate state
    - Next-day forecast
    - Forecast uncertainty
    - Heat-risk score
    - Heat-risk category
    - Risk-component contributions
    - Risk-model validation metadata
    """

    current_date: pd.Timestamp
    forecast_date: pd.Timestamp

    current_temperature_C: float
    climatological_temperature_C: float
    current_anomaly_C: float
    previous_anomaly_C: float

    predicted_temperature_C: float
    predicted_anomaly_C: float

    prediction_lower_C: float
    prediction_upper_C: float

    residual_mean_C: float
    residual_std_C: float

    heat_risk_score: float
    heat_risk_category: str

    anomaly_risk_component: float
    persistence_risk_component: float
    forecast_risk_component: float

    extreme_heat_risk: bool

    risk_threshold: float
    risk_precision: float
    risk_recall: float
    risk_f1: float
    risk_specificity: float


def load_forecast_uncertainty():
    """
    Load empirical forecast-error calibration.

    The calibration was derived from the validation
    forecast residual distribution.
    """

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    uncertainty_path = (
        project_root
        / "models"
        / "forecast_uncertainty.csv"
    )

    uncertainty = pd.read_csv(
        uncertainty_path
    ).iloc[0]

    return {
        "residual_mean_C": float(
            uncertainty[
                "residual_mean_C"
            ]
        ),

        "residual_std_C": float(
            uncertainty[
                "residual_std_C"
            ]
        ),

        "residual_lower_C": float(
            uncertainty[
                "residual_lower_C"
            ]
        ),

        "residual_upper_C": float(
            uncertainty[
                "residual_upper_C"
            ]
        )
    }


def create_digital_twin_state(
    model,
    monthly_climatology,
    current_date,
    forecast_date,
    current_anomaly_C,
    previous_anomaly_C
):
    """
    Construct the complete Digital Twin state.

    The Digital Twin combines:

    1. Current climate state
    2. Next-day anomaly forecast
    3. Predicted temperature
    4. Empirical forecast uncertainty
    5. Calibrated heat-risk assessment
    6. Risk-model validation metadata
    """

    current_date = pd.Timestamp(
        current_date
    )

    forecast_date = pd.Timestamp(
        forecast_date
    )

    current_anomaly_C = float(
        current_anomaly_C
    )

    previous_anomaly_C = float(
        previous_anomaly_C
    )

    # ==================================================
    # CURRENT CLIMATOLOGICAL BASELINE
    # ==================================================

    current_climatology = float(
        monthly_climatology.loc[
            current_date.month
        ]
    )

    # ==================================================
    # CURRENT OBSERVED TEMPERATURE
    # ==================================================

    current_temperature = (
        current_climatology
        + current_anomaly_C
    )

    # ==================================================
    # FORECAST MODEL INPUT
    # ==================================================

    input_data = pd.DataFrame({
        "anomaly": [
            current_anomaly_C
        ],
        "anomaly_lag_1": [
            previous_anomaly_C
        ]
    })

    # ==================================================
    # NEXT-DAY ANOMALY PREDICTION
    # ==================================================

    predicted_anomaly = float(
        model.predict(
            input_data
        )[0]
    )

    # ==================================================
    # FORECAST CLIMATOLOGICAL BASELINE
    # ==================================================

    forecast_climatology = float(
        monthly_climatology.loc[
            forecast_date.month
        ]
    )

    # ==================================================
    # NEXT-DAY PREDICTED TEMPERATURE
    # ==================================================

    predicted_temperature = (
        forecast_climatology
        + predicted_anomaly
    )

    # ==================================================
    # FORECAST UNCERTAINTY
    # ==================================================

    uncertainty = (
        load_forecast_uncertainty()
    )

    residual_mean = (
        uncertainty[
            "residual_mean_C"
        ]
    )

    residual_std = (
        uncertainty[
            "residual_std_C"
        ]
    )

    residual_lower = (
        uncertainty[
            "residual_lower_C"
        ]
    )

    residual_upper = (
        uncertainty[
            "residual_upper_C"
        ]
    )

    # --------------------------------------------------
    # Asymmetric empirical prediction interval
    # --------------------------------------------------

    prediction_lower = (
        predicted_anomaly
        + residual_lower
    )

    prediction_upper = (
        predicted_anomaly
        + residual_upper
    )

    # ==================================================
    # HEAT RISK ENGINE
    # ==================================================

    heat_risk = calculate_heat_risk(
        current_anomaly_C=(
            current_anomaly_C
        ),

        previous_anomaly_C=(
            previous_anomaly_C
        ),

        predicted_anomaly_C=(
            predicted_anomaly
        )
    )

    # ==================================================
    # LOAD RISK CALIBRATION
    # ==================================================

    risk_calibration = (
        load_heat_risk_calibration()
    )

    risk_threshold = (
        risk_calibration[
            "risk_score_threshold"
        ]
    )

    risk_precision = (
        risk_calibration[
            "precision"
        ]
    )

    risk_recall = (
        risk_calibration[
            "recall"
        ]
    )

    risk_f1 = (
        risk_calibration[
            "f1"
        ]
    )

    risk_specificity = (
        risk_calibration[
            "specificity"
        ]
    )

    # ==================================================
    # CONSTRUCT DIGITAL TWIN STATE
    # ==================================================

    return DigitalTwinState(

        current_date=current_date,

        forecast_date=forecast_date,

        current_temperature_C=float(
            current_temperature
        ),

        climatological_temperature_C=float(
            current_climatology
        ),

        current_anomaly_C=float(
            current_anomaly_C
        ),

        previous_anomaly_C=float(
            previous_anomaly_C
        ),

        predicted_temperature_C=float(
            predicted_temperature
        ),

        predicted_anomaly_C=float(
            predicted_anomaly
        ),

        prediction_lower_C=float(
            prediction_lower
        ),

        prediction_upper_C=float(
            prediction_upper
        ),

        residual_mean_C=float(
            residual_mean
        ),

        residual_std_C=float(
            residual_std
        ),

        heat_risk_score=float(
            heat_risk.score
        ),

        heat_risk_category=(
            heat_risk.category
        ),

        anomaly_risk_component=float(
            heat_risk.anomaly_component
        ),

        persistence_risk_component=float(
            heat_risk.persistence_component
        ),

        forecast_risk_component=float(
            heat_risk.forecast_component
        ),

        extreme_heat_risk=(
            heat_risk.extreme_heat_risk
        ),

        risk_threshold=float(
            risk_threshold
        ),

        risk_precision=float(
            risk_precision
        ),

        risk_recall=float(
            risk_recall
        ),

        risk_f1=float(
            risk_f1
        ),

        risk_specificity=float(
            risk_specificity
        )
    )