import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('Global_temperatures_for_streamlit.csv')

# Streamlit app
st.title('Global Temperatures Visualization')

# Dropdown for country selection
country = st.selectbox('Select Country:', df['Country'].unique(), index=list(df['Country'].unique()).index('Ireland'))

# Dropdown for year selection
year = st.selectbox('Select Year:', df['Year'].unique(), index=list(df['Year'].unique()).index(df['Year'].max()))

# Function to create and display the map
def display_map(selected_country, selected_year):
    country_year_data = df[(df['Country'] == selected_country) & (df['Year'] == selected_year)]
    
    if not country_year_data.empty:
        coords = [country_year_data.iloc[0]['Latitude'], country_year_data.iloc[0]['Longitude']]
        
        m = folium.Map(location=coords, zoom_start=6)
        
        for _, row in country_year_data.iterrows():
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                icon=folium.DivIcon(html=f"""
                    <div style="
                        background-color: rgba(255, 255, 255, 0.8);
                        border: 2px solid #4CAF50;
                        border-radius: 8px;
                        box-shadow: 3px 3px 5px #888888;
                        padding: 5px;
                        width: 100px;
                        font-family: Arial, sans-serif;
                        font-size: 12pt;
                        color: #4CAF50;
                        text-align: center;">
                        <strong>{selected_country}</strong><br>
                        {row['YearlyAverageTemperature']:.1f}°C
                    </div>""")
            ).add_to(m)
        
        title_html = f'<h3 align="center" style="font-size:20px"><b>Average Temperature in {selected_year} for {selected_country}</b></h3>'
        m.get_root().html.add_child(folium.Element(title_html))
        
        st_folium(m, width=700, height=500)
    else:
        st.write(f"No data available for {selected_country} in {selected_year}")

# Function to create and display the chart
def display_chart(selected_country):
    country_data = df[df['Country'] == selected_country]
    
    if not country_data.empty:
        fig = px.line(country_data, x='Year', y='YearlyAverageTemperature', title=f'Yearly Average Temperature for {selected_country} (1890 - 2012)')
        
        z = np.polyfit(country_data['Year'], country_data['YearlyAverageTemperature'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=country_data['Year'], y=p(country_data['Year']), mode='lines', name='Trendline (10 years)', line=dict(dash='dash', color='red')))
        
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {selected_country}")

# Function to display the highest and lowest recorded temperature and corresponding months
def display_temperature_info(selected_country, selected_year):
    country_year_data = df[(df['Country'] == selected_country) & (df['Year'] == selected_year)]
    
    if not country_year_data.empty:
        highest_temp = country_year_data['AverageTemperature'].max()
        lowest_temp = country_year_data['AverageTemperature'].min()
        highest_temp_date = pd.to_datetime(country_year_data.loc[country_year_data['AverageTemperature'].idxmax()]['Month'])
        lowest_temp_date = pd.to_datetime(country_year_data.loc[country_year_data['AverageTemperature'].idxmin()]['Month'])
        
        highest_temp_month = highest_temp_date.strftime('%B')
        lowest_temp_month = lowest_temp_date.strftime('%B')
        
        st.sidebar.write(f"**Highest and Lowest Temperatures for {selected_country} in {selected_year}:**")
        st.sidebar.write(f"Highest Recorded: {highest_temp:.2f}°C in {highest_temp_month}")
        st.sidebar.write(f"Lowest Recorded: {lowest_temp:.2f}°C in {lowest_temp_month}")
    else:
        st.sidebar.write(f"No data available for {selected_country} in {selected_year}")

# Display the map and chart based on the selected country and year
display_map(country, year)
display_chart(country)
display_temperature_info(country, year)
