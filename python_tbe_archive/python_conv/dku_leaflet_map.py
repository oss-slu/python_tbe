import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import webshot
import webshot.cli

# Load necessary libraries
import warnings
warnings.filterwarnings("ignore")

# Load the data
indir = ''
flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_lt'
flin = f"{indir}{flroot}.csv"
flrootout = f"p{flroot}"

## Variable to plot (sct means select)
varsct = 'pm25'
varunits = 'ug/m3'

## Filter data by date/time
## Season, time of day and min/max time to select.
## Use None if you do not want to filter
seasonsct = 'Dry'  # None, 'Dry', 'Wet'
timeofdaysct = 'Night'  # None, 'Day', 'Night', 'Trans'
timeminsct = None
timemaxsct = None
# timeminsct = pd.to_datetime('2022-12-15 00:00')
# timemaxsct = pd.to_datetime('2023-02-15 00:00')

timezone_output = 'Asia/Dhaka'

## Read the data
tb = pd.read_csv(flin)

tb['date'] = pd.to_datetime(tb['date'])
if ftype == 1:
    tb['date'] = tb['date'].dt.tz_localize('UTC').dt.tz_convert(timezone_output)
else:
    tb['date'] = tb['date'].dt.tz_localize(timezone_output)

print(f"Read {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

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

## filter data by time of day if required
if timeofdaysct is not None:
    tb = tb[tb['timeofday'] == timeofdaysct]
    if len(tb) == 0:
        raise ValueError(f"No data found, check data selection in timeofdaysct: {timeofdaysct}")

## filter data by start/end time if required
if timeminsct is not None:
    tb = tb[tb['date'] >= timeminsct]
    if len(tb) == 0:
        raise ValueError(f"No data found, check data selection in timeminsct: {timeminsct}")

if timemaxsct is not None:
    tb = tb[tb['date'] <= timemaxsct]
    if len(tb) == 0:
        raise ValueError(f"No data found, check data selection in timemaxsct: {timemaxsct}")

print(f"Found {len(tb)} rows from {min(tb['date'])} to {max(tb['date'])}")

## Date string for plot titles
date_str = f"{min(tb['date']).date()} to {max(tb['date']).date()}"
date_str_flname = f"{min(tb['date']).strftime('%Y%m%d')}_{max(tb['date']).strftime('%Y%m%d')}"
if seasonsct is not None:
    date_str = f"{date_str_flname} ({seasonsct})"
    date_str_flname = f"{date_str_flname}_{seasonsct.lower()}"

## get mean and count by site and season
tbsct = tb.groupby('sitename').agg(
    pm25_mean=('pm25', 'mean'),
    pm25_stdev=('pm25', 'std'),
    pm25_count=('pm25', 'count'),
    latitude=('latitude', 'mean'),
    longitude=('longitude', 'mean')
).reset_index()

tbsct['pm25_mean'] = tbsct['pm25_mean'].round(1)
tbsct['pm25_stdev'] = tbsct['pm25_stdev'].round(1)

if domap:
    latmin, latmax = tbsct['latitude'].min(), tbsct['latitude'].max()
    lonmin, lonmax = tbsct['longitude'].min(), tbsct['longitude'].max()
    lat1 = latmin - dlatlon
    lat2 = latmax + dlatlon
    lon1 = lonmin - dlatlon
    lon2 = lonmax + dlatlon
    cmin_data = np.floor(tbsct['pm25_mean'].min())
    cmax_data = np.ceil(tbsct['pm25_mean'].max())
    print(f"Data Range: {cmin_data} to {cmax_data}")
    cmin_lgd = cmin_data if cmin_ref is None else cmin_ref
    cmax_lgd = cmax_data if cmax_ref is None else cmax_ref

    cmap = sns.color_palette("rainbow", as_cmap=True)
    pal = sns.color_palette("rainbow", 10)
    pal = dict(zip(np.linspace(cmin_lgd, cmax_lgd, 10), pal))
    lgd_str = "PM2.5 Conc </br> (\u03BCg / m\u00B3) </br>"

    pmap = sns.scatterplot(data=tbsct, x='longitude', y='latitude', hue='pm25_mean', palette=pal, size=10,
                           legend=False)
    pmap.set(xlabel="Longitude", ylabel="Latitude")
    pmap.set_title("TSI Bluesky Data")
    pmap.figure.set_size_inches(fgwidth / 100, fgheight / 100)

    if plot2file:
        flout = f"{flrootout}_map_pm25.png"
        flhtml = f"{flrootout}_map_pm25.html"
        pmap.figure.savefig(flout, dpi=200)
        print(f"You can open {flhtml} in a web browser to view the figure interactively")

print("Type 'pmap' in the console to show the map")
