import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data, plot_wind_rose

# Set page config
st.set_page_config(
    page_title="MoonLight Energy Solutions Dashboard",
    page_icon="☀️",
    layout="wide"
)

# Add title and description
st.title("MoonLight Energy Solutions Analytics Dashboard")
st.markdown("""
    This dashboard provides insights into solar farm data to optimize energy investments 
    and enhance operational efficiency.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your data (CSV)", type=['csv'])

if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)
    
    # Display basic statistics
    st.header("Data Overview")
    st.write(df.describe())
    
    # Create two columns for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Solar Generation Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind='line', y='Solar Generation', ax=ax)
        plt.xlabel('Time')
        plt.ylabel('Generation (kWh)')
        st.pyplot(fig)
        plt.close()
        
    with col2:
        st.subheader("Wind Rose Diagram")
        if 'Wind Direction' in df.columns and 'Wind Speed' in df.columns:
            wind_rose = plot_wind_rose(df)
            st.pyplot(wind_rose)
            plt.close()
    
    # Temperature vs Efficiency Analysis
    st.header("Temperature vs Efficiency Analysis")
    if 'Temperature' in df.columns and 'Efficiency' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind='scatter', x='Temperature', y='Efficiency', ax=ax)
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Efficiency (%)')
        st.pyplot(fig)
        plt.close()
    
    # Show raw data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)

else:
    st.info('Please upload a CSV file to begin analysis')
