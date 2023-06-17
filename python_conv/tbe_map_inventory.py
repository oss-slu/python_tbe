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
flroot = 'saq_bluesky_bgd_20211001_20230430_inv'
flrootout = f"p{flroot}"
flin = f"{indir}_tbe.csv"

sites_str = 'bgd'
ndata_min_summary = 100

domap = 1
dlatlon = 0.01
cmin_ref = 0  # if None, use min(data)
cmax_ref = 220  # if None, use max(data)
cmax_ref = None
cmin_ref = None

plot2file = 1  # save to html (zoomable), to png if dowebshot == 1
dowebshot = 1  # creating png requires chrome

# Read the data
tb = pd.read_csv(flin)
tb_sites = tb.copy()

tb_sites['siteid'] = tb_sites['siteid'].astype('category')
tbsct = tb_sites

if domap:
    latmin, latmax = tbsct['latitude'].min(), tbsct['latitude'].max()
    lonmin, lonmax = tbsct['longitude'].min(), tbsct['longitude'].max()
    lat1 = latmin - dlatlon
    lat2 = latmax + dlatlon
    lon1 = lonmin - dlatlon
    lon2 = lonmax + dlatlon

    cmin_data = np.floor(tbsct['nrecords'].min())
    cmax_data = np.ceil(tbsct['nrecords'].max())
    print(f"Data Range: {cmin_data} to {cmax_data}")
    cmin_lgd = cmin_data if cmin_ref is None else cmin_ref
    cmax_lgd = cmax_data if cmax_ref is None else cmax_ref

    cmap = sns.color_palette("rainbow", as_cmap=True)
    pal = sns.color_palette("rainbow", 10)
    pal = dict(zip(np.linspace(cmin_lgd, cmax_lgd, 10), pal))
    lgd_str = "NRecords"

    pmap = sns.scatterplot(data=tbsct, x='longitude', y='latitude', hue='nrecords', palette=pal, size=10,
                           legend=False)
    pmap.set(xlabel="Longitude", ylabel="Latitude")
    pmap.set_title("Inventory Data")
    pmap.figure.set_size_inches(ggwidth / 100, ggheight / 100)

    if plot2file:
        flhtml = f"{flrootout}_map.html"
        pmap.figure.savefig(flhtml, dpi=ggdpi)
        print(f"You can open {flhtml} in a web browser to view the figure interactively")
        if dowebshot:
            flout = f"{flrootout}_map.png"
            webshot.cli.screenshot(flhtml, flout)
            print(f"Figure saved to {flout}")

print("Type 'pmap' in the console to show the map")
