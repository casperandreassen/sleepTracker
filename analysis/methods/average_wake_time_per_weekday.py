from tabulate import tabulate


def average_wake_times_per_weekday(sleep_data):
    """
    Calculate the average awake time per weekday based on sleep data.

    Args:
        sleep_data (DataFrame): The sleep data containing 'Timestamp' and 'Action' columns.

    Returns:
        None
    """
    # Calculate awake time per wake-sleep cycle
    sleep_data['Awake Time'] = sleep_data.groupby((sleep_data['Action'] == 'wake').cumsum())['Timestamp'].diff()

    # Filter out sleep records
    sleep_records = sleep_data[sleep_data['Action'] == 'sleep']

    # Calculate average awake time per weekday
    average_awake_time_per_weekday = sleep_records.groupby(sleep_records['Timestamp'].dt.day_name())['Awake Time'].mean()

    # Import the tabulate library
    # Sort the weekdays in the desired order
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    average_awake_time_per_weekday = average_awake_time_per_weekday.reindex(weekday_order)

    # Create a list of lists to store the table data
    table_data = []
    for weekday, average_time in average_awake_time_per_weekday.items():
        hours = average_time.total_seconds() // 3600
        minutes = (average_time.total_seconds() % 3600) // 60
        table_data.append([weekday, f"{int(hours)}:{int(minutes)}"])

    # Print the table
    print(tabulate(table_data, headers=["Weekday", "Average Awake Time"]))
