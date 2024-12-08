import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
def summary_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    regional_stats = {}

    for region in df['Region'].unique():
        region_data = df[df['Region'] == region][numeric_cols]
        stats = region_data.describe().round(2)
        regional_stats[region] = stats
        
        print(f"\nSummary Statistics for {region}:")
        print("=" * 80)
        print(stats)
        print("\n")

def missing_values(df):
    missing_values = df.isnull().sum()
    missing_percentages = (missing_values / len(df) * 100).round(2)

    # Create a summary DataFrame
    missing_summary = pd.DataFrame({
        'Missing Values': missing_values,
        'Percentage Missing': missing_percentages
    })

    print("Missing Values Analysis:")
    print("=" * 80)
    print(missing_summary)

    # Check missing values by region
    missing_by_region = df.groupby('Region').apply(
        lambda x: x.isnull().sum()
    ).round(2)

    print("\nMissing Values by Region:")
    print("=" * 80) 
    print(missing_by_region)

def negative_values(df):
    radiation_cols = ['GHI', 'DNI', 'DHI']
    negative_radiation = df[radiation_cols].lt(0).sum()
    print("Negative Values in Radiation Measurements:")
    print("=" * 80)
    print(negative_radiation)

    # Check sensor readings ranges
    sensor_cols = ['ModA', 'ModB'] 
    sensor_stats = df[sensor_cols].agg(['min', 'max', 'mean'])
    print("\nSensor Reading Ranges:")
    print("=" * 80)
    print(sensor_stats)

    # Validate wind speed measurements
    wind_cols = ['WS', 'WSgust']
    wind_stats = df[wind_cols].agg(['min', 'max', 'mean'])
    print("\nWind Speed Measurement Ranges:")
    print("=" * 80)
    print(wind_stats)

    # Check for other anomalous values
    print("\nOther Potential Anomalies:")
    print("=" * 80)

    # Check temperature ranges
    temp_cols = ['Tamb', 'TModA', 'TModB']
    temp_stats = df[temp_cols].agg(['min', 'max', 'mean'])
    print("\nTemperature Ranges:")
    print(temp_stats)

    # Check relative humidity range (should be 0-100%)
    rh_range = df['RH'].agg(['min', 'max', 'mean'])
    print("\nRelative Humidity Range:")
    print(rh_range)

    # Check pressure range
    bp_range = df['BP'].agg(['min', 'max', 'mean'])
    print("\nBarometric Pressure Range:")
    print(bp_range)

def outliers(df):
    z_score_threshold = 3

    # Calculate z-scores for key measurements
    key_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS']
    for col in key_cols:
        z_col = f'{col}_zscore'
        df[z_col] = df.groupby('Region')[col].transform(lambda x: zscore(x))
        
    # Identify outliers
    outliers = pd.DataFrame()
    for col in key_cols:
        z_col = f'{col}_zscore'
        outliers[col] = (abs(df[z_col]) > z_score_threshold).sum()

    print("Number of outliers detected (|z-score| > 3):")
    print("=" * 50)
    print(outliers.T)

    # Visualize outlier distribution for key metrics
    plt.figure(figsize=(15, 8))
    for i, col in enumerate(['GHI', 'DNI', 'DHI']):
        plt.subplot(1, 3, i+1)
        sns.boxplot(data=df, x='Region', y=col)
        plt.title(f'{col} Distribution with Outliers')
        plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Print extreme outlier examples
    print("\nExample records with extreme outliers:")
    print("=" * 50)
    extreme_outliers = df[
        (abs(df['GHI_zscore']) > z_score_threshold) |
        (abs(df['DNI_zscore']) > z_score_threshold) |
        (abs(df['DHI_zscore']) > z_score_threshold)
    ].head()
    print(extreme_outliers[['Timestamp', 'Region', 'GHI', 'DNI', 'DHI']])

def time_series(df):
    # Extract month and hour from timestamp
    df['Month'] = pd.to_datetime(df['Timestamp']).dt.month
    df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour

    # Calculate monthly averages
    monthly_avg = df.groupby('Month').agg({
        'GHI': 'mean',
        'DNI': 'mean', 
        'DHI': 'mean',
        'Tamb': 'mean'
    }).round(2)

    # Plot monthly patterns
    plt.figure(figsize=(15, 10))

    plt.subplot(2,2,1)
    monthly_avg['GHI'].plot(kind='bar')
    plt.title('Average Monthly GHI')
    plt.xlabel('Month')
    plt.ylabel('GHI (W/m²)')

    plt.subplot(2,2,2)
    monthly_avg['DNI'].plot(kind='bar')
    plt.title('Average Monthly DNI')
    plt.xlabel('Month')
    plt.ylabel('DNI (W/m²)')

    plt.subplot(2,2,3)
    monthly_avg['DHI'].plot(kind='bar')
    plt.title('Average Monthly DHI')
    plt.xlabel('Month')
    plt.ylabel('DHI (W/m²)')

    plt.subplot(2,2,4)
    monthly_avg['Tamb'].plot(kind='bar')
    plt.title('Average Monthly Temperature')
    plt.xlabel('Month')
    plt.ylabel('Temperature (°C)')

    plt.tight_layout()
    plt.show()

    # 2. Daily patterns
    hourly_avg = df.groupby('Hour').agg({
        'GHI': 'mean',
        'DNI': 'mean',
        'DHI': 'mean',
        'Tamb': 'mean'
    }).round(2)

    plt.figure(figsize=(15, 10))

    plt.subplot(2,2,1)
    hourly_avg['GHI'].plot(kind='line', marker='o')
    plt.title('Average Daily GHI Pattern')
    plt.xlabel('Hour of Day')
    plt.ylabel('GHI (W/m²)')

    plt.subplot(2,2,2)
    hourly_avg['DNI'].plot(kind='line', marker='o')
    plt.title('Average Daily DNI Pattern')
    plt.xlabel('Hour of Day')
    plt.ylabel('DNI (W/m²)')

    plt.subplot(2,2,3)
    hourly_avg['DHI'].plot(kind='line', marker='o')
    plt.title('Average Daily DHI Pattern')
    plt.xlabel('Hour of Day')
    plt.ylabel('DHI (W/m²)')

    plt.subplot(2,2,4)
    hourly_avg['Tamb'].plot(kind='line', marker='o')
    plt.title('Average Daily Temperature Pattern')
    plt.xlabel('Hour of Day')
    plt.ylabel('Temperature (°C)')

    plt.tight_layout()
    plt.show()


def cleaning_impact(df):
    # Calculate average readings for the day before and after cleaning
    df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
    cleaning_dates = df[df['Cleaning'] == 1]['Date'].unique()

    before_after_df = pd.DataFrame()
    for date in cleaning_dates:
        # Get day before and day of cleaning
        day_before = df[df['Date'] == date - pd.Timedelta(days=1)][['ModA', 'ModB']].mean()
        day_of = df[df['Date'] == date][['ModA', 'ModB']].mean()
        
        before_after_df = pd.concat([before_after_df, pd.DataFrame({
            'Day': ['Before', 'After'],
            'ModA': [day_before['ModA'], day_of['ModA']],
            'ModB': [day_before['ModB'], day_of['ModB']]
        })])

    # Calculate averages
    before_after_avg = before_after_df.groupby('Day')[['ModA', 'ModB']].mean()

    # Plot
    plt.figure(figsize=(10, 6))
    before_after_avg.plot(kind='bar')
    plt.title('Average Sensor Readings: Day Before vs Day of Cleaning')
    plt.xlabel('Day Relative to Cleaning')
    plt.ylabel('Average Sensor Reading')
    plt.legend()
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Print statistics
    print("\nAverage Readings Before vs After Cleaning:")
    print("=" * 50)
    print(before_after_avg.round(2))

    # Calculate percentage change
    pct_change = ((before_after_avg.loc['After'] - before_after_avg.loc['Before']) / before_after_avg.loc['Before'] * 100).round(2)
    print("\nPercentage Change After Cleaning:")
    print("=" * 50)
    print(pct_change)



