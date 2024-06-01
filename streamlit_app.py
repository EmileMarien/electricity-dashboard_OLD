import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# Filter data based on selected time period
filtered_data = meter_data[meter_data['time'] >= (datetime.now() - timedelta(minutes=time_period))]

# Display line chart of the selected meter data
st.line_chart(filtered_data[['time', meter]].set_index('time'))

# Calculate statistical metrics
avg_value = filtered_data[meter].mean()
min_value = filtered_data[meter].min()
max_value = filtered_data[meter].max()

# Display statistical metrics
st.subheader(f'Statistical Metrics for {meter} (Last {time_period} minutes)')
st.write(f'**Average:** {avg_value:.2f}')
st.write(f'**Minimum:** {min_value:.2f}')
st.write(f'**Maximum:** {max_value:.2f}')

# Function to update data every minute
def update_data():
    meter_data = get_meter_data()
    filtered_data = meter_data[meter_data['time'] >= (datetime.now() - timedelta(minutes=time_period))]
    st.line_chart(filtered_data[['time', meter]].set_index('time'))
    avg_value = filtered_data[meter].mean()
    min_value = filtered_data[meter].min()
    max_value = filtered_data[meter].max()
    st.subheader(f'Statistical Metrics for {meter} (Last {time_period} minutes)')
    st.write(f'**Average:** {avg_value:.2f}')
    st.write(f'**Minimum:** {min_value:.2f}')
    st.write(f'**Maximum:** {max_value:.2f}')

# Set Streamlit to run the update_data function every minute
st.experimental_rerun()

# Extra Guidance:
# 1. You could add an option to download the displayed data as a CSV file using `st.download_button`.
# 2. Include additional statistical metrics or visualizations as needed.
# 3. Implement a notification system for specific conditions (e.g., if the meter reading exceeds a certain threshold).
# 4. Allow comparison between multiple meters by selecting multiple meters and displaying them on the same graph.
# 5. Integrate with a real database or an API for actual data instead of the dummy function.
