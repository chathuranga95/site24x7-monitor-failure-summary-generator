import csv
from collections import defaultdict
import sys

if len(sys.argv) != 4:
    print("Usage: python failure-summary.py <input_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = "output/daily_monitor_failure_summary.csv"  # Output file path

start_date = sys.argv[2]
end_date = sys.argv[3]

# Full month names for mapping
full_month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def getAllDates(start_date, end_date):
    start_date_elements = start_date.split(" ")
    end_date_elements = end_date.split(" ")

    start_month = full_month_names.index(start_date_elements[0]) + 1
    end_month = full_month_names.index(end_date_elements[0]) + 1

    start_day = int(start_date_elements[1])
    end_day = int(end_date_elements[1])

    start_year = int(start_date_elements[2])
    end_year = int(end_date_elements[2])

    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                break
            for day in range(1, 32):
                if year == start_year and month == start_month and day < start_day:
                    continue
                if year == end_year and month == end_month and day > end_day:
                    break
                dates.append(f"{full_month_names[month - 1]} {day} {year}")
    return dates


# Function to summarize daily failure counts
def summarize_daily_failures(input_csv, output_csv):
    # Data structure to hold daily failure counts
    daily_failure_counts = defaultdict(int)

    # Get all dates between start and end date
    allDates = getAllDates(start_date, end_date)
    for failure_date in allDates:
        daily_failure_counts[failure_date]  = 0

    # Read the input CSV
    with open(input_csv, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse the date using the custom method
            failure_start_time_elements = row["Start Time"].split(" ")
            failure_date = (
                failure_start_time_elements[0] + " "
                + failure_start_time_elements[1] + " "
                + failure_start_time_elements[3]
            )

            # Increment the failure count for the specific date
            daily_failure_counts[failure_date] += 1

    # Sort the summary by date
    sorted_daily_summary = sorted(
        daily_failure_counts.items(),
        key=lambda x: (
            int(x[0].split(" ")[2]),  # Year
            full_month_names.index(x[0].split(" ")[0]),  # Month index
            int(x[0].split(" ")[1])  # Day
        )
    )

    # Write the summarized data to a new CSV
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Failure Count"])  # Header
        writer.writerows(sorted_daily_summary)

# Call the function
summarize_daily_failures(input_csv, output_csv)
print(f"Daily summary saved to {output_csv}")
