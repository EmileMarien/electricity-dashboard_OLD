import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import time

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Electricity Meter Dashboard',
    page_icon=':electric_plug:',  # This is an emoji shortcode. Could be a URL too.
)

# Hide Streamlit's default menu and footer using custom CSS
hide_streamlit_style = """
            <style>
            div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            #MainMenu {
                visibility: hidden;
                height: 0%;
            }
            header {
                visibility: hidden;
                height: 0%;
            }
            footer {
                visibility: hidden;
                height: 0%;
            }
            button[title="View fullscreen"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Dummy function to simulate live electricity meter data
@st.cache_data(ttl=60)
def get_meter_data():
    """Simulate fetching electricity meter data."""
    now = datetime.now(pytz.timezone('Europe/Berlin'))
    times = [now - timedelta(minutes=i) for i in range(60*24*7)]  # Simulate data for the past week
    meter1 = np.random.random(len(times)) * 100  # Simulated data for meter 1
    meter2 = np.random.random(len(times)) * 100  # Simulated data for meter 2
    meter3 = np.random.random(len(times)) * 100  # Simulated data for meter 3

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

# Date and time pickers for start and end date
start_date = st.date_input('Start date', value=(datetime.now(pytz.timezone('Europe/Berlin')) - timedelta(days=7)).date())
end_date = st.date_input('End date', value=datetime.now(pytz.timezone('Europe/Berlin')).date())

start_time = st.time_input('Start time', value=datetime.now(pytz.timezone('Europe/Berlin')).time())
end_time = st.time_input('End time', value=datetime.now(pytz.timezone('Europe/Berlin')).time())

# Combine date and time
start_datetime = datetime.combine(start_date, start_time).replace(tzinfo=pytz.timezone('Europe/Berlin'))
end_datetime = datetime.combine(end_date, end_time).replace(tzinfo=pytz.timezone('Europe/Berlin'))

# Interval for data points
interval = st.selectbox('Select interval (minutes)', [1, 5, 10, 15, 30, 60])

# Filter data based on selected date and time range
filtered_data = meter_data[(meter_data['time'] >= start_datetime) & (meter_data['time'] <= end_datetime)]
filtered_data = filtered_data.set_index('time').resample(f'{interval}T').mean().reset_index()

# Containers for dynamic content
chart_container = st.empty()
metrics_container = st.empty()

# Function to update data every minute
def update_data():
    meter_data = get_meter_data()
    filtered_data = meter_data[(meter_data['time'] >= start_datetime) & (meter_data['time'] <= end_datetime)]
    filtered_data = filtered_data.set_index('time').resample(f'{interval}T').mean().reset_index()

    # Update line chart
    chart_container.line_chart(filtered_data[['time', meter]].set_index('time'))

    # Calculate statistical metrics
    avg_value = filtered_data[meter].mean()
    min_value = filtered_data[meter].min()
    max_value = filtered_data[meter].max()

    # Display statistical metrics
    with metrics_container:
        st.subheader(f'Statistical Metrics for {meter} (From {start_datetime} to {end_datetime})')
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
# 1. You could add an option to download the displayed data as a CSV file using `st.download_button`.
# 2. Include additional statistical metrics or visualizations as needed.
# 3. Implement a notification system for specific conditions (e.g., if the meter reading exceeds a certain threshold).
# 4. Allow comparison between multiple meters by selecting multiple meters and displaying them on the same graph.
# 5. Integrate with a real database or an API for actual data instead of the dummy function.
