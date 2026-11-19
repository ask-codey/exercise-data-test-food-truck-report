# Exercise: Test the Food Truck Report

Exercise code for the lesson **Exercise: Test the Food Truck Report** in the Python for Data Analysis course on [ask-codey.com](https://www.ask-codey.com).

The Greenway Food Truck's weekly report is built by `report_functions.py`: the total of every sale, the week's numbers, a table for each location, and a chart of the items sold. The code works, but nobody wrote tests for it, so the next person who changes it could put a wrong number in front of the owner and nobody would know. You'll write the tests. Then `python check.py` plants four real bugs in copies of `report_functions.py`, one at a time, and tells you whether your tests caught each one.

## What's here

- `report_functions.py`: the report's five functions, `add_total`, `summarize`, `sales_by_location`, `save_location_table` and `items_chart`. The docstring under each says what it does. It works. Ready to use: don't change it.
- `seed.py`: makes eight weeks of sales, our own made-up data, in `data/incoming/` (about 400 sales a week), the same weeks as *Exercise: Food Truck Weekly Report*. It uses a fixed random seed, so it writes the same files on every computer; `python seed.py --next` adds the week after. Ready to use.
- `report.py`: prints the newest week's numbers with `report_functions.py`, so you can see the functions at work on real data. Ready to use.
- `tests/test_report_functions.py`: your tests. It has one worked example. For you to finish.
- `tests/conftest.py`: sets matplotlib's Agg backend, so the chart tests draw in memory with no window. Ready to use.
- `check.py` and `check/`: the check that runs your tests against four copies of `report_functions.py` with a bug planted in each. You don't need to change them, and it's more fun not to read the copies in `check/planted-bugs/` until you're done.
- `requirements.txt`: the packages this exercise needs, each at an exact version: pandas, matplotlib and pytest. Ready to use.
- `pytest.ini`: tells pytest where the tests are and where to find `report_functions.py`. Ready to use.
- `.gitignore`: tells Git to leave out the virtual environment, the files Python and pytest make as they run, and the `data/` folder, which `seed.py` makes again whenever it's needed. Ready to use.

## Before you start

The packages go in a virtual environment: a private set of packages for this folder only. In VS Code's terminal, in this folder, run these three commands.

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On a Mac (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- The first command makes the virtual environment, in a folder named `.venv`.
- The second turns it on for this terminal: the prompt starts with `(.venv)` from then on.
- The third installs the packages `requirements.txt` lists into it.

*Virtual Environments and pip* explains all three. The `.venv` folder is in `.gitignore`, so Git leaves it out: these commands make it again on any computer.

If PowerShell answers that running scripts is disabled on this system, run this once, then run the second command again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Each new terminal starts with the virtual environment off. If the prompt doesn't start with `(.venv)`, run the second command again. (VS Code often turns it on for you.)

Then make the data, once:

```bash
python seed.py
```

It prints a line for each of the eight weeks it writes, the first `Wrote data/incoming/week-2026-09-07.csv: 409 sales.` Your tests don't need these files: they build their own small weeks. `report.py` uses them.

## The rules to test

These are the weekly report's functions from *Exercise: Food Truck Weekly Report*, made sturdier for a missing price and an empty week, with two more for a table of the locations. Every function takes a DataFrame of sales with the columns `location`, `item`, `quantity` and `price` (the price of one item, in dollars), and leaves that DataFrame unchanged.

- **`add_total(df)`** returns a new DataFrame: the sales with a `total` column, each sale's `quantity` times its `price`. A sale with no price has no total yet: its total is missing (`NaN`), not `0.0`.
- **`summarize(df)`** returns a dictionary with five keys: `sales` (the sum of `total`, rounded to 2 decimal places, leaving out sales with no price), `items_sold` (the sum of `quantity`), `unpriced` (how many sales have no price), `best_item` (the item with the largest quantity sold, not the most sales) and `best_location` (the location with the largest sum of `total`). An empty week gives `0.0` for `sales`, `0` for the two counts and `None` for the two names.
- **`sales_by_location(df)`** returns a new DataFrame with one row per location, the largest sales first, its rows numbered from 0, and the columns `location`, `items_sold` and `sales`.
- **`save_location_table(df, path)`** writes `sales_by_location(df)` to a CSV file at `path`, with a header row and no row numbers.
- **`items_chart(df)`** returns `(fig, ax)`: a bar chart with one bar per item, its height the item's quantity sold, the most sold first. Its title is `Items sold this week`, its x-axis label `Item` and its y-axis label `Number sold`.

## The two small weeks

Test on these, built by hand in your test file (the worked example shows how to make a DataFrame). Every answer below was worked out from them on paper.

**The four-sale week:**

| location | item | quantity | price |
|---|---|---|---|
| City Park | Street Tacos | 5 | 9.00 |
| Office Row | Horchata | 1 | 3.50 |
| Office Row | Horchata | 2 | 3.50 |
| Stadium | Elote | 2 | 4.50 |

**The week with a missing price:**

| location | item | quantity | price |
|---|---|---|---|
| City Park | Street Tacos | 2 | 9.00 |
| Stadium | Elote | 1 | (missing: `None`) |

## Write your tests

```bash
python -m pytest
```

It runs every test in `tests/`. Cover every behavior below with at least one test.

**`add_total`**

1. On one sale, 2 Street Tacos at 9.00 at City Park, the `total` column is `[18.0]`. (This is the worked example.)
2. On the four-sale week, it returns the same four rows and columns with a `total` column added: `45.0`, `3.5`, `7.0` and `9.0`. Check the whole table with `pd.testing.assert_frame_equal`.
3. On the week with a missing price, the Street Tacos sale's total is `18.0`, and the Elote sale's total is missing (`NaN`), not `0.0`.
4. It leaves the table it's given unchanged: after `add_total(sales)`, `sales` still equals a copy made before the call.

**`summarize`**

5. On the four-sale week, it returns exactly `{"sales": 64.5, "items_sold": 10, "unpriced": 0, "best_item": "Street Tacos", "best_location": "City Park"}`.
6. The best item counts the quantity sold, not the sales: on the four-sale week it's `"Street Tacos"` (5 on one sale), not `"Horchata"` (3 on two sales).
7. On the week with a missing price, `sales` is `18.0` and `unpriced` is `1`.
8. On an empty week (the four columns, no rows), it returns exactly `{"sales": 0.0, "items_sold": 0, "unpriced": 0, "best_item": None, "best_location": None}`.

**`sales_by_location`**

9. On the four-sale week, it returns this table, rows numbered 0 to 2 (check it with `assert_frame_equal`):

   | location | items_sold | sales |
   |---|---|---|
   | City Park | 5 | 45.0 |
   | Office Row | 3 | 10.5 |
   | Stadium | 2 | 9.0 |

**`save_location_table`**

10. On the four-sale week, the file at `path` holds exactly `"location,items_sold,sales\nCity Park,5,45.0\nOffice Row,3,10.5\nStadium,2,9.0\n"`.

**`items_chart`**

11. On the four-sale week, the title is `Items sold this week`, the x-axis label `Item` and the y-axis label `Number sold`.
12. On the four-sale week, there are 3 bars, their heights `5`, `3` and `2`, left to right, under the labels `Street Tacos`, `Horchata` and `Elote`.

## Check your work

```bash
python check.py
```

It runs your tests five times and prints a numbered line for each run:

1. **On the working `report_functions.py`.** There must be tests, and every one must pass. If one fails here, the code is right and the test is wrong: work its expected value out again from the rules and the small weeks.
2. **On a copy that picks the best item by the number of sales, not the quantity sold.**
3. **On a copy that counts a missing price as a price of 0.**
4. **On a copy where `add_total` changes the table it was given.**
5. **On a copy that puts the chart's bars in alphabetical order, not the most sold first.**

A planted bug counts as caught when at least one of your tests fails on its copy. If all your tests pass on a broken copy, that bug would reach the weekly report, and the line says what kind of test to add.

On the starter, check 1 passes (the worked example passes) and checks 2 to 5 don't: that's expected, because one test can't catch four bugs yet. When the last line says *All 5 checks pass*, your tests protect the report.

To see the functions at work on the newest week, run:

```bash
python report.py
```

## The rules

- Don't change `report_functions.py`. It works; the tests are your work.
- Write your tests in `tests/test_report_functions.py` and bring the functions in from `report_functions` (`from report_functions import ...`), as the worked example does, so the check can swap in its planted-bug copies.
- Name every test after its behavior's number and what it checks, such as `test_7_summarize_a_week_with_a_missing_price`.
- Close each chart's figure at the end of its test with `plt.close(fig)`.
- Don't change `check.py`, the copies in `check/`, `conftest.py`, `seed.py` or `report.py`.

## Tips

- Work out each expected value by hand first, from the rules and the small weeks. A test that copies whatever the code returns proves nothing.
- Write a small function in your test file that builds the four-sale week, such as `def four_sales():`, and call it in each test, so every test gets a fresh copy.
- `pd.testing.assert_frame_equal(result, expected)` compares two whole tables: columns, values, row numbers and each column's type. Write `45.0` and `9.0`, not `45` and `9`, for a column of decimals.
- `NaN` isn't equal to anything, itself included: check one missing value with `pd.isna(value)`.
- To prove a function leaves its table alone, make `before = sales.copy()`, call the function, then compare `sales` with `before`.
- An empty week with the right columns: the four-sale week's table with `.iloc[0:0]`, or a DataFrame whose four columns are empty lists.
- For `save_location_table`, give your test the `tmp_path` fixture and write into it: `path = tmp_path / "locations.csv"`. Then `path.read_text(encoding="utf-8")` reads the whole file back as one string.
- A chart's bars are in `ax.patches`, left to right; `bar.get_height()` is each one's value, and `[label.get_text() for label in ax.get_xticklabels()]` gives the names under them.

## Hand it in

When it works, push your solution to a public repo of your own on GitHub, then paste that repo's address into **Submit your exercise** on the lesson page at [ask-codey.com](https://www.ask-codey.com). That's what completes the lesson. The lesson page shows the Git commands, step by step.
