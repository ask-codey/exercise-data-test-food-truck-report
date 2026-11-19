# Shared set-up for the tests. You don't need to change this file.
# matplotlib draws with the Agg backend here: it makes charts in memory, with no window to open,
# so the chart tests run the same on every computer, with or without a screen.
import matplotlib

matplotlib.use("Agg")
