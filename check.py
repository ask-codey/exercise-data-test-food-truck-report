"""The check for this exercise: are your tests good enough to catch real bugs?

It runs your tests (every test in tests/) five times, each time in a copy of this folder:
  1) with the working report_functions.py: there must be tests, and every one must pass;
  2) to 5) with a copy of report_functions.py that has one bug planted in it: at least one of
     your tests must fail.

Run it with: python check.py (with the virtual environment on). You don't need to change this file,
and it's more fun not to read the planted bugs in check/planted-bugs/ until you're done.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

PLANTED_BUGS = [
    ("bug-1", "the best item picked by the number of sales, not the quantity sold",
     "Test the best item of the four-sale week: Street Tacos, 5 on one sale, beats Horchata, 3 on two."),
    ("bug-2", "a missing price counted as a price of 0",
     "Test a sale with no price: its total is missing (NaN), not 0.0, and summarize counts it as unpriced."),
    ("bug-3", "add_total changing the table it was given",
     "Copy the table, call add_total, and check the table still equals its copy with assert_frame_equal."),
    ("bug-4", "the chart's bars in alphabetical order, not the most sold first",
     "Check every bar's height, in order: 5, 3, 2 for the four-sale week."),
]


def run_your_tests(module_file):
    """Copies your tests and pytest.ini into a new folder with module_file as report_functions.py, runs pytest
    there, and gives back pytest's exit code: 0 every test passed, 1 a test failed, 5 there were no tests."""
    with tempfile.TemporaryDirectory() as folder:
        copy = Path(folder)
        shutil.copytree(HERE / "tests", copy / "tests", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(HERE / "pytest.ini", copy / "pytest.ini")
        shutil.copy(module_file, copy / "report_functions.py")
        run = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
            cwd=copy, capture_output=True, text=True,
        )
        return run.returncode


print("Checking your tests against the working report_functions.py and four copies with a bug planted in each.")
print()

checks_passed = 0
working = run_your_tests(HERE / "report_functions.py")
if working == 0:
    print("1) your tests pass on the working report_functions.py: yes")
    checks_passed += 1
elif working == 5:
    print("1) your tests pass on the working report_functions.py: not yet")
    print("   There are no tests yet: write them in tests/test_report_functions.py.")
else:
    print("1) your tests pass on the working report_functions.py: not yet")
    print("   A test fails on the working code, so the test is the one to fix. Run pytest to see which,")
    print("   and work its expected value out again from the README.")

for number, (folder, bug, tip) in enumerate(PLANTED_BUGS, start=2):
    print(f"{number}) your tests catch planted bug {number - 1}, {bug}: ", end="")
    if working != 0:
        print("not yet")
        print("   Get check 1 passing first: a bug only counts as caught when your tests pass on the working code.")
    elif run_your_tests(HERE / "check" / "planted-bugs" / folder / "report_functions.py") != 0:
        print("yes")
        checks_passed += 1
    else:
        print("not yet")
        print("   Every one of your tests passed on the copy with this bug, so it would reach the weekly report.")
        print(f"   {tip}")

print()
if checks_passed == 5:
    print("All 5 checks pass: your tests catch every planted bug.")
else:
    print(f"{checks_passed} of 5 checks pass so far.")
    sys.exit(1)
