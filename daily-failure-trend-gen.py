import csv
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

if len(sys.argv) != 4:
    print("Usage: python failure-summary.py <input_csv>")
    print(len(sys.argv))
    sys.exit(1)

input_csv = sys.argv[1]
output_folder = "output/charts"  # Folder to save charts
output_csv = "output/sorted_monitor_failures_summary.csv"  # Output file path

# Full month names for mapping
full_month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

start_date = sys.argv[2]
end_date = sys.argv[3]

def writeFailureSummary(failure_summary, output_csv):
    # Flatten and sort the summary
    sorted_summary = []
    for monitor_name in sorted(failure_summary.keys()):
        # Sort by the year, month, and day without using datetime
        sorted_dates = sorted(
            failure_summary[monitor_name].keys(),
            key=lambda x: (
                int(x.split(" ")[2]),  # Year
                full_month_names.index(x.split(" ")[0]),  # Month index
                int(x.split(" ")[1])  # Day
            )
        )
        for failure_date in sorted_dates:
            sorted_summary.append((monitor_name, failure_date, failure_summary[monitor_name][failure_date]))
        # Add an empty row after each monitor name batch
        sorted_summary.append(())

    # Write the summarized data to a new CSV
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Monitor Name", "Date", "Failure Count"])  # Header
        writer.writerows(sorted_summary)

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

# Function to parse data and generate charts
def generate_monitor_charts(input_csv, output_folder):
    # Data structure to hold failures
    failure_summary = defaultdict(lambda: defaultdict(int))

    with open(input_csv, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            monitor_name = row["Monitor Name"]

            # Get all dates between start and end date
            allDates = getAllDates(start_date, end_date)
            for failure_date in allDates:
                failure_summary[monitor_name][failure_date]  = 0

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
            monitor_name = row["Monitor Name"]

            # Increment the failure count for the monitor on the specific date
            failure_summary[monitor_name][failure_date] += 1
    
    writeFailureSummary(failure_summary, output_csv)

    # Create charts for each monitor
    for monitor_name, date_counts in failure_summary.items():
        # Sort dates
        sorted_dates = sorted(
            date_counts.keys(),
            key=lambda x: (
                int(x.split(" ")[2]),  # Year
                full_month_names.index(x.split(" ")[0]),
                int(x.split(" ")[1])  # Day
            )
        )

        # Prepare data for plotting
        dates = sorted_dates
        counts = [date_counts[date] for date in dates]

        # Plot the chart
        plt.figure(figsize=(10, 6))
        plt.plot(dates, counts, marker="o", linestyle="-", color="b")
        plt.title(f"{monitor_name}", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Failure Count", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()

        # Save the chart
        chart_file = f"{output_folder}/{monitor_name.replace(' ', '_').replace('[', '').replace(']', '')}.png"
        plt.savefig(chart_file)
        plt.close()
        print(f"Chart saved for monitor: {monitor_name} -> {chart_file}")

# Call the function
generate_monitor_charts(input_csv, output_folder)
