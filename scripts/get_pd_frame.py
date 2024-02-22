import pandas as pd
from os import getcwd
from scripts.generate_test_data import generate_data

def get_pd_frame(filename=None, num_days=0):
    """
    Returns a pandas DataFrame for sleep data analysis.

    Parameters:
    filename (str, optional): The name of the CSV file containing sleep data.
                              If not provided, data will be generated using `generate_data`.
                              Default is None.
    num_days (int, optional): The number of days of data to generate if `filename` is not provided.
                              Ignored if `filename` is provided.
                              Default is 0.

    Returns:
    pandas.DataFrame: A DataFrame containing sleep data with columns:
                      - 'Action': Either wake or sleep
                      - 'Timestamp': Datetime objects representing sleep/wake times.
    """
    if filename == None and num_days > 0:
        sleep_data = generate_data(num_days)        
    elif filename != None:
        # Read sleep data from CSV file
        sleep_data = pd.read_csv(getcwd() + '/data/' + filename)
    else:
        raise Exception("No filename provided and no days specified for file generation.")

    # Convert string timestamps to datetime objects
    sleep_data['Timestamp'] = pd.to_datetime(sleep_data['Timestamp'])
    return sleep_data 