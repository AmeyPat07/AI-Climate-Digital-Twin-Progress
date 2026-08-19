import pandas as pd


def forecast_next_day(
    model,
    today_anomaly,
    yesterday_anomaly
):
    """
    Forecast the next-day temperature anomaly.

    Parameters
    ----------
    model : trained regression model
        Final trained forecasting model.
    today_anomaly : float
        Today's temperature anomaly (°C).
    yesterday_anomaly : float
        Yesterday's temperature anomaly (°C).

    Returns
    -------
    float
        Predicted next-day anomaly (°C).
    """

    input_data = pd.DataFrame({
        "anomaly": [today_anomaly],
        "anomaly_lag_1": [yesterday_anomaly]
    })

    prediction = model.predict(input_data)[0]

    return float(prediction)


def assess_extreme_heat_risk(
    today_anomaly,
    threshold=3.0
):
    """
    Assess next-day extreme-heat risk using
    the validated persistence rule.

    Parameters
    ----------
    today_anomaly : float
        Today's temperature anomaly (°C).
    threshold : float, default=3.0
        Extreme-heat anomaly threshold (°C).

    Returns
    -------
    bool
        True when extreme-heat risk is detected.
    """

    return bool(today_anomaly >= threshold)


def digital_twin_forecast(
    model,
    monthly_climatology,
    today_anomaly,
    yesterday_anomaly,
    forecast_date
):
    """
    Generate a complete next-day Digital Twin forecast.

    Returns predicted anomaly, predicted temperature,
    and extreme-heat risk.
    """

    forecast_date = pd.Timestamp(forecast_date)

    predicted_anomaly = forecast_next_day(
        model,
        today_anomaly,
        yesterday_anomaly
    )

    climatological_temperature = float(
        monthly_climatology.loc[
            forecast_date.month
        ]
    )

    predicted_temperature = (
        climatological_temperature
        + predicted_anomaly
    )

    extreme_heat_risk = assess_extreme_heat_risk(
        today_anomaly
    )

    return {
        "forecast_date": forecast_date,
        "today_anomaly_C": float(today_anomaly),
        "yesterday_anomaly_C": float(yesterday_anomaly),
        "climatological_temperature_C":
            climatological_temperature,
        "predicted_anomaly_C":
            predicted_anomaly,
        "predicted_temperature_C":
            float(predicted_temperature),
        "extreme_heat_risk":
            extreme_heat_risk
    }


def simulate_anomaly_scenario(
    model,
    monthly_climatology,
    today_anomaly,
    yesterday_anomaly,
    forecast_date
):
    """
    Simulate a hypothetical climate state and
    calculate the next-day Digital Twin response.
    """

    return digital_twin_forecast(
        model=model,
        monthly_climatology=monthly_climatology,
        today_anomaly=today_anomaly,
        yesterday_anomaly=yesterday_anomaly,
        forecast_date=forecast_date
    )