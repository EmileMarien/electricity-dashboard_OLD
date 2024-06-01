import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Electricity Meter Dashboard',
    page_icon=':electric_plug:',  # This is an emoji shortcode. Could be a URL too.
)

# Dummy function to simulate live electricity meter data
@st.cache_data(ttl=60)
def get_meter_data():
    """Simulate fetching electricity meter data."""
    now = datetime.now()
    times = [now - timedelta(minutes=i) for i in range(60)]
    meter1 = np.random.random(60) * 100  # Simulated data for meter 1
    meter2 = np.random.random(60) * 100  # Simulated data for meter 2
    meter3 = np.random.random(60) * 100  # Simulated data for meter 3

    data = {
        'time': times,
        'Meter 1': meter1,
        'Meter 2': meter2,
        'Meter 3': meter3,
    }

    return pd.DataFrame(data)

# Fetch initial data
meter_data = get_meter_data()

# Set the title that appears at the top of the page.
st.title(':electric_plug: Electricity Meter Dashboard')

# Dropdown to select meter
meter = st.selectbox(
    'Select Meter',
    ['Meter 1', 'Meter 2', 'Meter 3']
)

# Time period slider (in minutes)
time_period = st.slider(
    'Select Time Period (in minutes)',
    min_value=5,
    max_value=60,
    value=30
)

# Containers for dynamic content
chart_container = st.empty()
metrics_container = st.empty()

# Function to update data every minute
def update_data():
    meter_data = get_meter_data()
    filtered_data = meter_data[meter_data['time'] >= (datetime.now() - timedelta(minutes=time_period))]
    
    # Update line chart
    chart_container.line_chart(filtered_data[['time', meter]].set_index('time'))
    
    # Calculate statistical metrics
    avg_value = filtered_data[meter].mean()
    min_value = filtered_data[meter].min()
    max_value = filtered_data[meter].max()
    
    # Display statistical metrics
    with metrics_container:
        st.subheader(f'Statistical Metrics for {meter} (Last {time_period} minutes)')
        st.write(f'**Average:** {avg_value:.2f}')
        st.write(f'**Minimum:** {min_value:.2f}')
        st.write(f'**Maximum:** {max_value:.2f}')

# Initial call to display data
update_data()

# Refresh data every minute
while True:
    time.sleep(60)
    update_data()

# Extra Guidance:
# 1. You could a
