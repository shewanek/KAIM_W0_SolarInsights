# Data Processing Script Documentation

## Overview
`data_process.py` is a comprehensive Python script for analyzing and processing solar radiation and weather data. It provides extensive functionality for data cleaning, statistical analysis, and visualization of environmental measurements.

## Key Functions

### Data Analysis Functions
- `summary_stats(df)`: Generates summary statistics grouped by region for numeric columns
- `missing_values(df)`: Analyzes missing values overall and by region
- `negative_values(df)`: Validates radiation measurements and sensor readings for negative/anomalous values
- `outliers(df)`: Detects and visualizes outliers using z-scores and box plots
- `time_series(df)`: Analyzes monthly and daily patterns in measurements
- `cleaning_impact(df)`: Evaluates the impact of cleaning on sensor readings

### Environmental Analysis Functions
- `correlation(df)`: Analyzes correlations between solar, temperature and wind variables
- `wind_analysis(df)`: Detailed wind pattern analysis including wind roses and directional statistics
- `humidity_analysis(df)`: Studies humidity relationships with temperature and radiation
- `distribution_analysis(df)`: Examines statistical distributions of key measurements
- `z_score_analysis(df)`: Identifies extreme values using standardized scores
- `bubble_plot(df)`: Creates multivariate visualizations of environmental relationships

### Data Cleaning Function
- `data_cleaning(df)`: Comprehensive data cleaning pipeline that:
  - Removes invalid values
  - Handles missing data
  - Removes outliers
  - Eliminates duplicates
  - Exports cleaned dataset

## Required Libraries
- numpy
- pandas 
- matplotlib
- seaborn
- scipy

## Input Data Format
The script expects a DataFrame with the following key columns:
- Timestamp
- Region
- GHI, DNI, DHI (radiation measurements)
- Tamb, TModA, TModB (temperature measurements)
- WS, WSgust, WD (wind measurements)
- RH (relative humidity)
- BP (barometric pressure)

## Output
- Detailed statistical analysis printed to console
- Multiple visualization plots
- Cleaned dataset saved as CSV

