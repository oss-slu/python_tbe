import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder

# Load necessary libraries
import warnings
warnings.filterwarnings("ignore")

# Set plot style
sns.set(style="ticks")

# Load the data
indir = ''
flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_lt'
flin = f"{indir}{flroot}.csv"
tb = pd.read_csv(flin)

# Variable to plot
varsct = 'pm25'
varunits = 'ug/m3'

# Filter data by season
seasonsct = None  # None, 'Dry', 'Wet'

timezone_output = 'Asia/Dhaka'

# Read the data
asites = tb['sitename'].unique()
tb['sitename'] = tb['sitename'].astype('category')

if ftype == 1:
    tb['date'] = pd.to_datetime(tb['date']).dt.tz_localize('UTC').dt.tz_convert(timezone_output)
else:
    tb['date'] = pd.to_datetime(tb['date']).dt.tz_localize(timezone_output)

print(f"Read {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

# Create vector of seasons for filtering
tb_season = pd.DataFrame({'name': ['Dry', 'Wet', 'Dry'], 'start_mmdd': [1, 401, 1101]})
tb['season0'] = pd.cut(
    100 * tb['date'].dt.month + tb['date'].dt.day,
    bins=[tb_season['start_mmdd'].iat[0] - 1] + tb_season['start_mmdd'].tolist(),
    labels=tb_season['name'],
    right=False
)

# Create time of day categories for plotting
tb['timeofday'] = pd.cut(
    tb['date'].dt.hour,
    bins=[-1, 8.5, 10.5, 16.5, 18.5, 24],
    labels=['Night', 'Trans', 'Day', 'Trans', 'Night']
)
tb['timeofday'] = tb['timeofday'].astype('category')

# Filter data by season if required
if seasonsct is not None:
    tb = tb[tb['season0'] == seasonsct]
    if len(tb) == 0:
        raise ValueError(f"No data found, check data selection in seasonsct: {seasonsct}")

print(f"Found {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

# Date string for plot titles
date_str = f"{min(tb['date']).date()} to {max(tb['date']).date()}"
date_str_flname = f"{min(tb['date']).strftime('%Y%m%d')}_{max(tb['date']).strftime('%Y%m%d')}"
if seasonsct is not None:
    date_str = f"{date_str_flname} ({seasonsct})"
    date_str_flname = f"{date_str_flname}_{seasonsct.lower()}"

# Correlogram code wants matching data in separate columns
tb_wide = tb.pivot(index='date', columns='sitename', values='pm25')

# Check data availability
nrow_all = len(tb_wide)
tb_wide = tb_wide.dropna(subset=asites, how='any')
nrow_allvalid = len(tb_wide)
print(f"{nrow_allvalid}/{nrow_all} rows with valid data for all sites")
if nrow_allvalid == 0:
    raise ValueError("No valid data found, stop here")

# Make correlogram with seaborn pairplot
sns.pairplot(tb_wide[asites], kind='reg', diag_kind='kde', markers='.')
plt.savefig(f"{flrootout}_corr.png")
print(f"Correlogram saved to file {flrootout}_corr.png")

# Correlation plot using seaborn scatterplot
p_xy = sns.scatterplot(data=tb_wide, x=asites[0], y=asites[1], hue='timeofday', alpha=0.4)
p_xy.set_title(f"CC {asites[0]}, {asites[1]}")
plt.savefig(f"{flrootout}_xy.png")
print(f"XY plot saved to file {flrootout}_xy.png")
