import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from windrose import WindroseAxes

def load_data(file):
    """
    Load and validate CSV data file
    
    Args:
        file: Uploaded CSV file object
    Returns:
        pandas DataFrame with validated data
    """
    try:
        df = pd.read_csv(file)
        # required_columns = ['Timestamp',	'GHI',	'DNI,'	'DHI',	'ModA',	'ModB',	'Tamb',	'RH',	'WS',	'WSgust',	'WSstdev',	'WD',	'WDstdev',	'BP',	'Cleaning',	'Precipitation',	'TModA',	'TModB',	'Region']
        
        # # Validate required columns exist
        # missing = [col for col in required_columns if col not in df.columns]
        # if missing:
        #     raise ValueError(f"Missing required columns: {', '.join(missing)}")
            
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def time_series(df):
    """
    Generate time series plots showing monthly and daily patterns of solar radiation and temperature
    
    Args:
        df: pandas DataFrame with solar and temperature data
    """
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

    # Create figure for monthly patterns
    fig1, axes1 = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot monthly patterns
    monthly_avg['GHI'].plot(kind='bar', ax=axes1[0,0])
    axes1[0,0].set_title('Average Monthly GHI')
    axes1[0,0].set_xlabel('Month')
    axes1[0,0].set_ylabel('GHI (W/m²)')

    monthly_avg['DNI'].plot(kind='bar', ax=axes1[0,1])
    axes1[0,1].set_title('Average Monthly DNI') 
    axes1[0,1].set_xlabel('Month')
    axes1[0,1].set_ylabel('DNI (W/m²)')

    monthly_avg['DHI'].plot(kind='bar', ax=axes1[1,0])
    axes1[1,0].set_title('Average Monthly DHI')
    axes1[1,0].set_xlabel('Month')
    axes1[1,0].set_ylabel('DHI (W/m²)')

    monthly_avg['Tamb'].plot(kind='bar', ax=axes1[1,1])
    axes1[1,1].set_title('Average Monthly Temperature')
    axes1[1,1].set_xlabel('Month')
    axes1[1,1].set_ylabel('Temperature (°C)')

    plt.tight_layout()
     
    return fig1
    
def correlation(df):
    """
    Create correlation plots for solar, temperature and wind variables
    
    Args:
        df: pandas DataFrame containing solar, temperature and wind measurements
    Returns:
        matplotlib figure with correlation heatmaps
    """
    try:
        # Create correlation matrix for solar and temperature variables
        solar_temp_vars = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'Tamb']
        solar_temp_corr = df[solar_temp_vars].corr()

        # Create correlation matrix for wind and solar variables 
        wind_solar_vars = ['GHI', 'DNI', 'DHI', 'WS', 'WSgust', 'WD']
        wind_solar_corr = df[wind_solar_vars].corr()

        # Set up the figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Plot solar-temperature correlations
        sns.heatmap(solar_temp_corr, 
                    annot=True,
                    cmap='RdBu',
                    center=0,
                    ax=ax1)
        ax1.set_title('Solar Radiation vs Temperature Correlations')

        # Plot wind-solar correlations
        sns.heatmap(wind_solar_corr,
                    annot=True, 
                    cmap='RdBu',
                    center=0,
                    ax=ax2)
        ax2.set_title('Wind vs Solar Radiation Correlations')

        plt.tight_layout()
        return fig
        
    except Exception as e:
        raise Exception(f"Error creating correlation plots: {str(e)}")

def humidity_analysis(df):
    """
    Create scatter plots analyzing relationships between relative humidity and other variables
    
    Args:
        df: pandas DataFrame containing RH, temperature and solar measurements
    Returns:
        matplotlib figure with humidity analysis plots
    """
    try:
        # Create scatter plots to examine RH relationships
        fig = plt.figure(figsize=(15, 10))

        plt.subplot(2,2,1)
        plt.scatter(df['RH'], df['Tamb'], alpha=0.5)
        plt.title('Relative Humidity vs Ambient Temperature')
        plt.xlabel('Relative Humidity (%)')
        plt.ylabel('Temperature (°C)')

        plt.subplot(2,2,2)
        plt.scatter(df['RH'], df['GHI'], alpha=0.5)
        plt.title('Relative Humidity vs Global Horizontal Irradiance')
        plt.xlabel('Relative Humidity (%)')
        plt.ylabel('GHI (W/m²)')

        plt.subplot(2,2,3)
        plt.scatter(df['RH'], df['TModA'], alpha=0.5, label='Module A')
        plt.scatter(df['RH'], df['TModB'], alpha=0.5, label='Module B')
        plt.title('Relative Humidity vs Module Temperatures')
        plt.xlabel('Relative Humidity (%)')
        plt.ylabel('Temperature (°C)')
        # plt.legend()

        plt.tight_layout()
        return fig

    except Exception as e:
        raise Exception(f"Error creating humidity analysis plots: {str(e)}")


def plot_wind_rose(df):
    """
    Create wind rose plot from wind speed and direction data
    
    Args:
        df: pandas DataFrame with 'WS' and 'WD' columns for wind speed and direction
    Returns:
        matplotlib figure with wind rose plot
    """
    try:
        # Create wind rose figure
        fig = plt.figure(figsize=(8, 8))
        ax = WindroseAxes.from_ax(fig=fig)
        
        # Plot wind rose using correct column names
        ax.bar(df['WD'], df['WS'], 
               bins=np.arange(0, 35, 5), # Wind speed bins
               normed=True,
               opening=0.8,
               edgecolor='white')
        
        # Customize appearance
        ax.set_legend(title='Wind Speed (m/s)')
        ax.set_title('Wind Rose Diagram')
        
        return fig
    except Exception as e:
        raise Exception(f"Error creating wind rose plot: {str(e)}")
