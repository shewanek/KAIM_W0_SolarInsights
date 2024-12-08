import numpy as np
import pandas as pd

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


