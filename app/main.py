import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data, plot_wind_rose, time_series, correlation, humidity_analysis
import streamlit as st

# Set page config
st.set_page_config(page_title="Solar Data Analysis", layout="wide")

# Add title
st.title("Solar Data Analysis Dashboard")
st.write("here is the link to the data: https://drive.google.com/file/d/1boBQADBu-_QuCWawStJpvZahgzkcerGB/view?usp=sharing")
# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Load data
        df = load_data(uploaded_file)

        # Add sidebar filters
        st.sidebar.header("Data Filters")
        
       
        # Region filter if multiple regions exist
        if 'Region' in df.columns:
            regions = df['Region'].unique()
            selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
        
        
        
        # Weather condition filters
        min_temp = float(df['Tamb'].min())
        max_temp = float(df['Tamb'].max())
        temp_range = st.sidebar.slider("Temperature Range (°C)", 
                                     min_value=min_temp,
                                     max_value=max_temp,
                                     value=(min_temp, max_temp))
        
        min_ws = float(df['WS'].min())
        max_ws = float(df['WS'].max())
        wind_range = st.sidebar.slider("Wind Speed Range (m/s)",
                                     min_value=min_ws,
                                     max_value=max_ws, 
                                     value=(min_ws, max_ws))
        
       
        if 'Region' in df.columns:
            mask = df['Region'].isin(selected_regions)
            
        # Filter the dataframe
        df = df[mask]
        
        # Show number of records after filtering
        st.sidebar.markdown(f"**Filtered Records:** {len(df):,}")

        # Basic statistics
        st.subheader("Data Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average GHI (W/m²)", f"{df['GHI'].mean():.2f}")
            st.metric("Average DNI (W/m²)", f"{df['DNI'].mean():.2f}")
            st.metric("Average DHI (W/m²)", f"{df['DHI'].mean():.2f}")
        
        with col2:
            st.metric("Average Module A Temp (°C)", f"{df['TModA'].mean():.2f}")
            st.metric("Average Module B Temp (°C)", f"{df['TModB'].mean():.2f}")
            st.metric("Average Ambient Temp (°C)", f"{df['Tamb'].mean():.2f}")
            
        with col3:
            st.metric("Average Wind Speed (m/s)", f"{df['WS'].mean():.2f}")
            st.metric("Average Relative Humidity (%)", f"{df['RH'].mean():.2f}")
            st.metric("Average Barometric Pressure (hPa)", f"{df['BP'].mean():.2f}")

        # Time series plots
        st.subheader("Time Series Analysis")
        
        # Get monthly and daily plots from time_series function
        monthly_fig= time_series(df)
        
        # Display the plots
        st.pyplot(monthly_fig)

        # Correlation plots
        st.subheader("Correlation Analysis")
        correlation_fig = correlation(df)
        st.pyplot(correlation_fig)


        # Humidity analysis
        st.subheader("Humidity Analysis")
        humidity_fig = humidity_analysis(df)
        st.pyplot(humidity_fig)

        # Remove this line since humidity_analysis() is already called above
        # and its figure is displayed with st.pyplot(humidity_fig)
        

        # Wind rose diagram
        st.subheader("Wind Analysis")
        wind_rose = plot_wind_rose(df)
        st.pyplot(wind_rose)

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
