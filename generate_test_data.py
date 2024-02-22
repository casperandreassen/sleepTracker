import random
from datetime import datetime, timedelta

def random_iso8601_time(date, hour, minute):
    # Generate a random time within the specified hour and minute
    return date.replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(minutes=random.randint(0, 59))

def generate_data(num_days):
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


# Generate 200 rows of sleep time series data
sleep_data = generate_data(1000)

with open('sleep_data.csv', 'w') as f:
    for event, time in sleep_data:
        f.write(f"{event},{time}\n")