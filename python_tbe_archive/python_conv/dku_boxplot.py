import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load necessary libraries
import warnings
warnings.filterwarnings("ignore")

# Set plot style
sns.set(style="ticks")

## Input directory and file name: indir, flroot
indir = ''
flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_15min_lt'
flin = f"{indir}{flroot}.csv"
flrootout = f"p{flroot}"

varselect = 'pm25'
timezone_output = 'Asia/Dhaka'
seasonsct = None  # None, 'Dry', 'Wet'

## Read data
tb = pd.read_csv(flin)

## Sites to select: either specify in asites, or use unique to select all
##asites = ['65. Sylhet MPU', '66. Sylhet Ambarkhana']
asites = tb['sitename'].unique()

if ftype == 1:
    tb['date'] = pd.to_datetime(tb['date']).dt.tz_localize('UTC').dt.tz_convert(timezone_output)
else:
    tb['date'] = pd.to_datetime(tb['date']).dt.tz_localize(timezone_output)

print(f"Read {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

tb['sitename'] = tb['sitename'].astype('category')

## create vector of seasons for filtering
tb_season = pd.DataFrame({'name': ['Dry', 'Wet', 'Dry'], 'start_mmdd': [1, 401, 1101]})
tb['season0'] = pd.cut(
    100 * tb['date'].dt.month + tb['date'].dt.day,
    bins=[tb_season['start_mmdd'].iat[0] - 1] + tb_season['start_mmdd'].tolist(),
    labels=tb_season['name'],
    right=False
)

## create time of day categories for plotting
tb['timeofday'] = pd.cut(
    tb['date'].dt.hour,
    bins=[-1, 8.5, 10.5, 16.5, 18.5, 24],
    labels=['Night', 'Trans', 'Day', 'Trans', 'Night']
)
tb['timeofday'] = tb['timeofday'].astype('category')

## filter data by season if required
if seasonsct is not None:
    tb = tb[tb['season0'] == seasonsct]
    if len(tb) == 0:
        raise ValueError(f"No data found, check data selection in seasonsct: {seasonsct}")

print(f"Found {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

## Create a diurnal boxplot
pdiel = sns.boxplot(data=tb, x=tb['date'].dt.hour, y='pm25', hue='sitename')
plt.savefig(f"{flrootout}_bp_diurnal.png")
print(f"Diurnal boxplot saved to file {flrootout}_bp_diurnal.png")

## Create a day of week boxplot
tb['wday'] = tb['date'].dt.dayofweek
pweekly = sns.boxplot(data=tb, x='wday', y='pm25', hue='sitename')
plt.savefig(f"{flrootout}_bp_weekly.png")
print(f"Weekly boxplot saved to file {flrootout}_bp_weekly.png")
