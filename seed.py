"""Makes the Greenway Food Truck's weekly sales files: our own made-up data. Ready to use.

Run it with: python seed.py
It writes eight weeks of sales into data/incoming/, one file a week, named by the Monday the
week starts on: week-2026-09-07.csv, week-2026-09-14.csv, ... week-2026-10-26.csv. Each file has
about 400 sales, one row per sale: sold_at, location, item, quantity, price, payment.

Run it with: python seed.py --next
It adds the week after the newest file in data/incoming/, as a new week of sales arriving, so you
can watch your report rebuild from it.

Every week has its own fixed random seed, so every run, on every computer, writes exactly the same
files. The tests don't need them: they build their own small weeks by hand.
"""
import argparse
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 2026
FIRST_MONDAY = date(2026, 9, 7)
WEEKS = 8
COLUMNS = ["sold_at", "location", "item", "quantity", "price", "payment"]

MENU = [
    # item, price, how often it's ordered
    ("Street Tacos", 9.00, 30),
    ("Burrito Bowl", 11.50, 22),
    ("Quesadilla", 8.50, 16),
    ("Loaded Fries", 6.50, 14),
    ("Elote", 4.50, 10),
    ("Horchata", 3.50, 8),
]

# Where the truck parks each day (Monday is 0), the hours it sells there, and how many sales a day.
SCHEDULE = {
    0: ("Office Row", 11, 14, 55),
    1: ("Office Row", 11, 14, 50),
    2: ("City Park", 11, 15, 45),
    3: ("Office Row", 11, 14, 55),
    4: ("Stadium", 17, 21, 80),
    5: ("Stadium", 17, 21, 75),
    6: ("City Park", 11, 16, 50),
}

PAYMENTS = [("card", 60), ("app", 25), ("cash", 15)]


def pick(rng, weighted):
    """One value from a list of (value, weight) pairs."""
    return rng.choices([v for v, _ in weighted], weights=[w for _, w in weighted])[0]


def make_week(monday):
    """Every sale of the week that starts on monday (a date), in the order they happened."""
    rng = random.Random(SEED * 1000 + (monday - FIRST_MONDAY).days)
    sales = []
    for day in range(7):
        location, opens, closes, usual = SCHEDULE[day]
        count = usual + rng.randint(-6, 6)
        start = datetime.combine(monday + timedelta(days=day), datetime.min.time()) + timedelta(hours=opens)
        minutes = (closes - opens) * 60
        for minute in sorted(rng.randrange(minutes) for _ in range(count)):
            item, price, _ = rng.choices(MENU, weights=[m[2] for m in MENU])[0]
            quantity = rng.choices([1, 2, 3], weights=[70, 22, 8])[0]
            sales.append({
                "sold_at": (start + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M"),
                "location": location,
                "item": item,
                "quantity": quantity,
                "price": f"{price:.2f}",
                "payment": pick(rng, PAYMENTS),
            })
    return sales


def write_week(folder, monday):
    """Writes the week that starts on monday into folder as week-<YYYY-MM-DD>.csv and returns its Path."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"week-{monday.isoformat()}.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(make_week(monday))
    return path


def write_weeks(folder, weeks=WEEKS):
    """Writes the first weeks (eight unless told otherwise) into folder and returns their Paths."""
    return [write_week(folder, FIRST_MONDAY + timedelta(weeks=n)) for n in range(weeks)]


def write_next_week(folder):
    """Writes the week after the newest week file in folder (or the first week, if there is none)."""
    files = sorted(Path(folder).glob("week-*.csv"))
    if not files:
        return write_week(folder, FIRST_MONDAY)
    newest = date.fromisoformat(files[-1].stem.removeprefix("week-"))
    return write_week(folder, newest + timedelta(weeks=1))


def count_sales(path):
    with Path(path).open(encoding="utf-8") as file:
        return sum(1 for _ in file) - 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make the food truck's weekly sales files.")
    parser.add_argument("--next", action="store_true", help="add the week after the newest file")
    args = parser.parse_args()
    folder = Path(__file__).parent / "data" / "incoming"
    written = [write_next_week(folder)] if args.next else write_weeks(folder)
    for path in written:
        print(f"Wrote data/incoming/{path.name}: {count_sales(path)} sales.")
