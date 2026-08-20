from dataclasses import dataclass


@dataclass
class WeatherState:
    """
    Describes the observed or simulated atmospheric
    weather condition used by the visual environment.

    This is intentionally separate from thermal climate
    state because temperature anomaly alone cannot
    determine cloud cover or precipitation.
    """

    condition: str
    label: str
    icon: str

    cloud_cover: float
    precipitation: float
    visibility: float


def create_weather_state(
    condition="clear"
):
    """
    Create a weather state for the environment renderer.

    Parameters
    ----------
    condition : str
        Current atmospheric condition.

        Supported conditions:
        - clear
        - partly_cloudy
        - cloudy
        - rain
        - storm
        - fog

    Returns
    -------
    WeatherState
        Atmospheric weather description.
    """

    states = {

        "clear": WeatherState(
            condition="clear",
            label="Clear",
            icon="☀️",
            cloud_cover=0.05,
            precipitation=0.0,
            visibility=1.0
        ),

        "partly_cloudy": WeatherState(
            condition="partly_cloudy",
            label="Partly Cloudy",
            icon="🌤️",
            cloud_cover=0.40,
            precipitation=0.0,
            visibility=0.90
        ),

        "cloudy": WeatherState(
            condition="cloudy",
            label="Cloudy",
            icon="☁️",
            cloud_cover=0.85,
            precipitation=0.0,
            visibility=0.75
        ),

        "rain": WeatherState(
            condition="rain",
            label="Rain",
            icon="🌧️",
            cloud_cover=0.95,
            precipitation=0.80,
            visibility=0.55
        ),

        "storm": WeatherState(
            condition="storm",
            label="Storm",
            icon="⛈️",
            cloud_cover=1.0,
            precipitation=1.0,
            visibility=0.40
        ),

        "fog": WeatherState(
            condition="fog",
            label="Fog",
            icon="🌫️",
            cloud_cover=0.70,
            precipitation=0.0,
            visibility=0.25
        )
    }

    if condition not in states:
        raise ValueError(
            f"Unsupported weather condition: {condition}"
        )

    return states[condition]