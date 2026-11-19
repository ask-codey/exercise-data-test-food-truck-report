# A copy of report_functions.py with one bug planted in it, for python check.py. Don't change it.
"""The Greenway Food Truck's report functions.

This file works, and it's ready to use: don't change it. Your job is the tests in
tests/test_report_functions.py, which prove it works and catch anyone who breaks it later.
Every function takes a DataFrame of sales with the columns location, item, quantity and price
(the price of one item, in dollars), and leaves that DataFrame unchanged.
"""
import matplotlib.pyplot as plt


def add_total(df):
    """Return a new DataFrame: the sales with a total column, each sale's quantity times its price.

    A sale with no price has no total yet: its total is missing (NaN), not 0.0, so a report can
    tell a sale nobody priced from a free one.

    2 Street Tacos at 9.00 -> total 18.0
    1 Elote with no price -> total NaN
    """
    result = df.copy()
    result["total"] = (result["quantity"] * result["price"]).round(2)
    return result


def summarize(df):
    """Return a dictionary of the week's headline numbers.

    {"sales": the sum of total, rounded to 2 decimal places, leaving out sales with no price,
     "items_sold": the sum of quantity, as an int,
     "unpriced": how many sales have no price,
     "best_item": the item with the largest quantity sold (not the most sales),
     "best_location": the location with the largest sum of total}

    When two items (or two locations) tie, the one that comes first alphabetically wins.
    An empty week gives 0.0 for sales, 0 for the two counts and None for the two names.
    """
    week = add_total(df)
    if len(week) == 0:
        return {"sales": 0.0, "items_sold": 0, "unpriced": 0, "best_item": None, "best_location": None}
    by_item = week.groupby("item")["quantity"].sum()
    by_location = week.groupby("location")["total"].sum()
    return {
        "sales": round(float(week["total"].sum()), 2),
        "items_sold": int(week["quantity"].sum()),
        "unpriced": int(week["total"].isna().sum()),
        "best_item": by_item.idxmax(),
        "best_location": by_location.idxmax(),
    }


def sales_by_location(df):
    """Return a new DataFrame with one row per location, the largest sales first.

    Its columns: location, items_sold (the sum of quantity) and sales (the sum of total,
    rounded to 2 decimal places), and its rows are numbered from 0.
    """
    week = add_total(df)
    table = week.groupby("location", as_index=False).agg(
        items_sold=("quantity", "sum"),
        sales=("total", "sum"),
    )
    table["sales"] = table["sales"].round(2)
    return table.sort_values("sales", ascending=False, ignore_index=True)


def save_location_table(df, path):
    """Write sales_by_location(df) to a CSV file at path, with a header row and no row numbers."""
    sales_by_location(df).to_csv(path, index=False, lineterminator="\n")


def items_chart(df):
    """Return (fig, ax): a bar chart of how many of each item sold, largest first.

    One bar per item, its height the item's total quantity, sorted from the most sold to the
    least; a tie keeps alphabetical order. Title: Items sold this week. X-axis label: Item.
    Y-axis label: Number sold.
    """
    counts = df.groupby("item")["quantity"].sum()
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    ax.bar(counts.index, counts.values)
    ax.set_title("Items sold this week")
    ax.set_xlabel("Item")
    ax.set_ylabel("Number sold")
    return fig, ax
