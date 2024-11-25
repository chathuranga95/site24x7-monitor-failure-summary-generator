# Site 24x7 monitor failure summary generator

This tool generates the following from a site 24x7 monitor outage csv
1. Total daily failures for a period in `.csv` format
2. Daily monitor failures grouped by monitor
- Data in `.csv` format -- `output/sorted_monitor_failures_summary.csv`
- Charts in `.png` format -- `output/charts/*`

## How to run

1. Clone the repo
2. Download site24x7 monitor outages in `.csv` format and remove non-csv metadata from the file.
2. Update `inputFilePath`, `startDate`, `endDate` on `.run.sh` file.
3. Run the following commands from the repo root
```bash
chmod +x run.sh
./run.sh
```