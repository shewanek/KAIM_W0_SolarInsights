import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
        required_columns = ['Solar Generation']
        
        # Validate required columns exist
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
            
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def plot_wind_rose(df):
    """
    Create wind rose plot from wind speed and direction data
    
    Args:
        df: pandas DataFrame with 'Wind Speed' and 'Wind Direction' columns
    Returns:
        matplotlib figure with wind rose plot
    """
    try:
        # Create wind rose figure
        fig = plt.figure(figsize=(8, 8))
        ax = WindroseAxes.from_ax(fig=fig)
        
        # Plot wind rose
        ax.bar(df['Wind Direction'], df['Wind Speed'], 
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
