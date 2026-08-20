from dataclasses import dataclass


@dataclass
class ClimateState:
    """
    Standardized representation of the current
    climate state used by the Digital Twin UI.
    """

    temperature_C: float
    anomaly_C: float
    climatology_C: float
    status: str
    extreme_heat_risk: bool


def classify_temperature_state(
    anomaly_C: float,
    extreme_heat_threshold: float = 3.0
) -> str:
    """
    Classify the thermal state from temperature anomaly.
    """

    if anomaly_C >= extreme_heat_threshold:
        return "Extreme heat"

    if anomaly_C > 1.0:
        return "Above normal"

    if anomaly_C < -1.0:
        return "Below normal"

    return "Near normal"


def build_climate_state(
    temperature_C: float,
    anomaly_C: float,
    climatology_C: float,
    extreme_heat_risk: bool
) -> ClimateState:
    """
    Build a standardized ClimateState object from
    the current Digital Twin outputs.
    """

    status = classify_temperature_state(
        anomaly_C=anomaly_C
    )

    return ClimateState(
        temperature_C=float(temperature_C),
        anomaly_C=float(anomaly_C),
        climatology_C=float(climatology_C),
        status=status,
        extreme_heat_risk=bool(extreme_heat_risk)
    )