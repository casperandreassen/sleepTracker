import random
from datetime import datetime, timedelta
from os import getcwd

def random_iso8601_time(date, hour, minute):
    """
    Generate a random time within the specified hour and minute.

    Parameters:
    - date (datetime): The date to generate the random time for.
    - hour (int): The hour of the day.
    - minute (int): The minute of the hour.

    Returns:
    - datetime: A random datetime object within the specified hour and minute.
    """
    return date.replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(minutes=random.randint(0, 59))


def generate_data(num_days):
    """
    Generate test data for sleep analysis.

    Args:
        num_days (int): The number of days for which to generate data.

    Returns:
        list: A list of tuples representing sleep records. Each tuple contains two elements:
              - The first element is a string indicating the type of record ("wake" or "sleep").
              - The second element is a string representing the ISO 8601 formatted timestamp.
    """
    data = []
    date = datetime(2020, 1, 1)
    wake_up_time = (7, 0)
    bedtime = (19, 0)
    nap_times = [(10, 0), (15, 0)]
    wake_times = [(12, 0), (17, 0)]
    for i in range(num_days):
        day = []
        naps = random.randint(1, 2)
        day.append(("wake", random_iso8601_time(date, wake_up_time[0], wake_up_time[1])))
        for nap in range(naps):
            day.append(("sleep", random_iso8601_time(date, nap_times[nap][0], nap_times[nap][1])))
            day.append(("wake", random_iso8601_time(date, wake_times[nap][0], wake_times[nap][1])))
        day.append(("sleep", random_iso8601_time(date, bedtime[0], bedtime[1])))
        date = date + timedelta(days=1)
        for record in day:
            data.append(record)
    return data


def generate_test_data(num_days, filename=None):
    """
    Generate test data for sleep analysis and write the output to csv 

    Parameters:
    - num_days (int): The number of days for which to generate sleep data.

    Returns:
    - None
    """
    if filename == None:
        filename = "sleep_data.csv"
    sleep_data = generate_data(num_days)
    with open(f"{getcwd}/data/{filename}", 'w') as f:
        for event, time in sleep_data:
            f.write(f"{event},{time}\n")