# Prints the newest week's numbers with the functions in report_functions.py, so you can see them at
# work on real data. Ready to use. Make the data first with: python seed.py
# Run it with: python report.py
from pathlib import Path

import pandas as pd

from report_functions import sales_by_location, summarize

newest = sorted(Path("data", "incoming").glob("week-*.csv"))[-1]
week = pd.read_csv(newest)
numbers = summarize(week)

print(f"Greenway Food Truck, {newest.name}")
print("1) sales:", numbers["sales"])
print("2) items sold:", numbers["items_sold"])
print("3) sales with no price:", numbers["unpriced"])
print("4) best item:", numbers["best_item"])
print("5) best location:", numbers["best_location"])
print()
print(sales_by_location(week).to_string(index=False))
