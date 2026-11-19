# Your tests for the Greenway Food Truck's report functions in report_functions.py. The README lists the
# 12 behaviors to cover, with the two small weeks to test them on.
# Run them with: python -m pytest (in the exercise folder, with the virtual environment on).
# Then run: python check.py, to see whether they catch the four bugs it plants in copies of report_functions.py.
import matplotlib.pyplot as plt
import pandas as pd

from report_functions import add_total, items_chart, sales_by_location, save_location_table, summarize


# Behavior 1, the worked example, to show the shape. Add your own tests below it.
def test_1_add_total_2_street_tacos_at_9_00_is_18_00():
    sales = pd.DataFrame({"location": ["City Park"], "item": ["Street Tacos"], "quantity": [2], "price": [9.00]})
    result = add_total(sales)
    assert result["total"].tolist() == [18.0]


# TODO: a test for each of the README's behaviors 2 to 12.
