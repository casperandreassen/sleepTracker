import pandas as pd
from datetime import datetime, timedelta

def get_average_wake_times_per_weekday(sleep_data):
    # Calculate awake time per wake-sleep cycle
    sleep_data['Awake Time'] = sleep_data.groupby((sleep_data['Action'] == 'wake').cumsum())['Timestamp'].diff()
    print(sleep_data)

    # Filter out sleep records
    sleep_records = sleep_data[sleep_data['Action'] == 'sleep']

    # Calculate average awake time per weekday
    average_awake_time_per_weekday = sleep_records.groupby(sleep_records['Timestamp'].dt.day_name())['Awake Time'].mean()

    # Print the result
    for weekday, average_time in average_awake_time_per_weekday.items():
        hours = average_time.total_seconds() // 3600
        minutes = (average_time.total_seconds() % 3600) // 60
        print(f"Average awake time on {weekday}: {int(hours)} hours {int(minutes)} minutes")

def get_pd():
    # Read sleep data from CSV file
    sleep_data = pd.read_csv('sleep_data.csv')

    # Convert string timestamps to datetime objects
    sleep_data['Timestamp'] = pd.to_datetime(sleep_data['Timestamp'])
    return sleep_data


get_average_wake_times_per_weekday(get_pd())

