#!/bin/sh

# Site 24x7 monitor failure report file path (CSV format).
# Important: Remove non-csv metadata headings from the file.
inputFilePath=""
# Start and end dates for daily failure summary.
# if data is not available for the selected date range,
# the script will consider that there are no monitor failures
startDate="November 4 2024" # Format: "Month DD YYYY"
endDate="November 25 2024" # Format: "Month DD YYYY"

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

rm -rf output
mkdir -p output/charts
python3 failure-summary.py "$inputFilePath" "$startDate" "$endDate"
python3 daily-failure-trend-gen.py "$inputFilePath" "$startDate" "$endDate"
