# AI-Powered Digital Twin of India's Climate

## Minor Project — Semester 5 Computer Engineering

An AI-powered Digital Twin of India's Climate using national datasets, developed as a Proof of Concept with Maharashtra as the pilot region.

## Project Objective

The project aims to develop a climate digital twin capable of:

- Processing national climate datasets
- Representing the climate state of a selected region
- Predicting future climate variables using AI/ML
- Visualizing climate conditions spatially
- Performing what-if scenario simulations

## Current Pilot Region

Maharashtra, India

## Current Climate Variable

Maximum Daily Temperature

## Data Source

India Meteorological Department (IMD)

Maximum Temperature 1° × 1° Gridded Dataset

Official source:
https://imdpune.gov.in/cmpg/Griddata/Max_1_Bin.html

## Current Dataset

Period:

2015–2024

Spatial resolution:

1° × 1°

Pilot-region grid locations:

26

Total observations:

94,978

## Current Pipeline

IMD Binary Data
        ↓
Binary Processing
        ↓
Spatial Filtering
        ↓
Maharashtra Climate Dataset
        ↓
Exploratory Data Analysis
        ↓
Prediction Baseline
        ↓
AI Model
        ↓
Digital Twin
        ↓
Visualization & Scenario Simulation

## Project Structure

data/
    boundaries/
    processed/
    raw/

notebooks/
    01_dataset_exploration.ipynb
    02_imd_binary_processing.ipynb
    03_build_climate_dataset.ipynb
    04_climate_eda.ipynb

## Status

### Completed

- IMD maximum-temperature binary decoding
- Maharashtra boundary integration
- Automated 2015–2024 processing
- 26 Maharashtra grid locations
- 3,653 daily dates
- 94,978 observations
- Climate exploratory data analysis
- Seasonal analysis
- Annual analysis
- Extreme-temperature analysis
- Temporal persistence analysis

### Next

- Persistence prediction baseline
- Feature engineering
- Machine-learning model
- Deep-learning model
- Model validation
- Digital twin state
- Interactive visualization
- What-if scenario simulation













# Maharashtra Climate Digital Twin

A climate-focused Digital Twin prototype for analyzing daily maximum temperature variability, detecting extreme heat events, forecasting next-day temperature anomalies, and simulating hypothetical climate states.

## 1. Project Overview

This project develops a data-driven Digital Twin for climate-state representation and short-term temperature forecasting.

The system uses historical daily maximum-temperature observations to:

- construct a monthly climatological baseline,
- calculate daily temperature anomalies,
- characterize long-term temperature variability,
- identify extreme heat and heatwave events,
- analyze temporal persistence using autocorrelation,
- develop and compare forecasting models,
- generate next-day temperature forecasts,
- assess extreme-heat risk,
- and simulate hypothetical climate scenarios.

The final system is implemented as an interactive Streamlit application.

---

## 2. Digital Twin Architecture

The project consists of four major layers:

```text
Historical Climate Data
        |
        v
Climate Preprocessing
        |
        v
Monthly Climatology
        |
        v
Daily Temperature Anomaly
        |
        v
Temporal Feature Engineering
        |
        v
Forecasting Model
        |
        +----------------------+
        |                      |
        v                      v
Next-Day Forecast       Extreme Heat Risk
        |                      |
        +----------+-----------+
                   |
                   v
          Digital Twin State
                   |
                   v
          Scenario Simulation
                   |
                   v
          Streamlit Dashboard