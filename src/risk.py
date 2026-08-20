from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class HeatRiskAssessment:
    """
    Interpretable heat-risk assessment produced by the
    Digital Twin risk engine.

    The score is a prototype analytical index calibrated
    against the 2023–2024 validation period.
    """

    score: float

    category: str

    anomaly_component: float

    persistence_component: float

    forecast_component: float

    extreme_heat_risk: bool


def _clamp(
    value,
    minimum=0.0,
    maximum=100.0
):
    """
    Restrict a value to the specified range.
    """

    return max(
        minimum,
        min(
            float(value),
            maximum
        )
    )


def load_heat_risk_calibration():
    """
    Load the validated heat-risk calibration artifact.

    Returns
    -------
    dict
        Calibration parameters and validation metrics.
    """

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    calibration_path = (
        project_root
        / "models"
        / "heat_risk_calibration.csv"
    )

    calibration = pd.read_csv(
        calibration_path
    ).iloc[0]

    return {
        "extreme_heat_observation_threshold_C":
            float(
                calibration[
                    "extreme_heat_observation_threshold_C"
                ]
            ),

        "risk_score_threshold":
            float(
                calibration[
                    "risk_score_threshold"
                ]
            ),

        "risk_score_max":
            float(
                calibration[
                    "risk_score_max"
                ]
            ),

        "validation_records":
            int(
                calibration[
                    "validation_records"
                ]
            ),

        "observed_extreme_events":
            int(
                calibration[
                    "observed_extreme_events"
                ]
            ),

        "precision":
            float(
                calibration[
                    "precision"
                ]
            ),

        "recall":
            float(
                calibration[
                    "recall"
                ]
            ),

        "f1":
            float(
                calibration[
                    "f1"
                ]
            ),

        "specificity":
            float(
                calibration[
                    "specificity"
                ]
            )
    }


def calculate_heat_risk(
    current_anomaly_C,
    previous_anomaly_C,
    predicted_anomaly_C
):
    """
    Calculate the calibrated 0–100 heat-risk score.

    Components
    ----------
    Current anomaly:
        Contribution from the magnitude of the current
        temperature anomaly.

    Persistence:
        Contribution from the current and previous
        temperature anomalies.

    Forecast:
        Contribution from the predicted next-day anomaly.

    Returns
    -------
    HeatRiskAssessment
        Complete risk assessment.
    """

    current = float(
        current_anomaly_C
    )

    previous = float(
        previous_anomaly_C
    )

    predicted = float(
        predicted_anomaly_C
    )

    # ==================================================
    # LOAD CALIBRATION
    # ==================================================

    calibration = (
        load_heat_risk_calibration()
    )

    risk_threshold = (
        calibration[
            "risk_score_threshold"
        ]
    )

    observation_threshold = (
        calibration[
            "extreme_heat_observation_threshold_C"
        ]
    )

    # ==================================================
    # CURRENT ANOMALY COMPONENT
    # ==================================================

    anomaly_component = _clamp(
        (current / 5.0) * 60.0
    )

    # ==================================================
    # PERSISTENCE COMPONENT
    # ==================================================

    persistence_signal = (
        (current + previous)
        / 2.0
    )

    persistence_component = _clamp(
        (persistence_signal / 5.0)
        * 25.0
    )

    # ==================================================
    # FORECAST COMPONENT
    # ==================================================

    forecast_component = _clamp(
        (predicted / 5.0)
        * 15.0
    )

    # ==================================================
    # TOTAL SCORE
    # ==================================================

    score = _clamp(
        anomaly_component
        + persistence_component
        + forecast_component
    )

    # ==================================================
    # CALIBRATED RISK CATEGORY
    # ==================================================

    if score >= risk_threshold:

        category = "Extreme"

    elif score >= 40:

        category = "High"

    elif score >= 25:

        category = "Moderate"

    else:

        category = "Low"

    # ==================================================
    # EXTREME HEAT FLAG
    #
    # This flag now uses the validation-calibrated
    # risk-score threshold rather than simply checking
    # the current anomaly.
    # ==================================================

    extreme_heat_risk = bool(
        score >= risk_threshold
    )

    return HeatRiskAssessment(

        score=float(
            score
        ),

        category=category,

        anomaly_component=float(
            anomaly_component
        ),

        persistence_component=float(
            persistence_component
        ),

        forecast_component=float(
            forecast_component
        ),

        extreme_heat_risk=(
            extreme_heat_risk
        )
    )
