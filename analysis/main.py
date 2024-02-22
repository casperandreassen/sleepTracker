from methods.average_wake_time_per_weekday import average_wake_times_per_weekday
from scripts.get_pd_frame import get_pd_frame
from scripts.generate_test_data import generate_test_data


def main():

    try:
        df = get_pd_frame(num_days=3)
    except Exception as e:
        print("Something went wrong." + e)
        return
    
    average_wake_times_per_weekday(df)


if __name__ == "__main__":
    main()