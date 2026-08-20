from dataclasses import dataclass


@dataclass
class EnvironmentState:
    """
    Visual environment state derived from the current
    thermal climate state.

    This layer describes the atmospheric visual mode
    associated with temperature/anomaly conditions.

    It does not claim to represent observed weather
    such as rainfall, cloud cover, humidity, or wind.
    """

    mode: str
    label: str
    icon: str
    intensity: float


def get_environment_state(
    climate_status: str,
    anomaly_C: float
) -> EnvironmentState:
    """
    Convert the current thermal climate state into
    a visual environment state.

    Parameters
    ----------
    climate_status : str
        Thermal classification produced by ClimateState.

    anomaly_C : float
        Current temperature anomaly in °C.

    Returns
    -------
    EnvironmentState
        Visual thermal environment description.
    """

    if climate_status == "Extreme heat":

        intensity = min(
            max((anomaly_C - 3.0) / 3.0, 0.0),
            1.0
        )

        return EnvironmentState(
            mode="extreme_heat",
            label="Extreme Heat",
            icon="☀️",
            intensity=intensity
        )

    if climate_status == "Above normal":

        intensity = min(
            max((anomaly_C - 1.0) / 2.0, 0.0),
            1.0
        )

        return EnvironmentState(
            mode="warm",
            label="Above Normal",
            icon="🌤️",
            intensity=intensity
        )

    if climate_status == "Below normal":

        intensity = min(
            max(abs(anomaly_C + 1.0) / 3.0, 0.0),
            1.0
        )

        return EnvironmentState(
            mode="cool",
            label="Below Normal",
            icon="🌥️",
            intensity=intensity
        )

    return EnvironmentState(
        mode="neutral",
        label="Near Normal",
        icon="⛅",
        intensity=0.0
    )