from analysis.average_wake_time_per_weekday import average_wake_times_per_weekday
from scripts.get_pd_frame import get_pd_frame


def main():
    try:
        df = get_pd_frame(filename="sleep_data.csv")
    except Exception:
        print("Something went wrong.")
    
    average_wake_times_per_weekday(df)

if __name__ == "__main__":
    main()