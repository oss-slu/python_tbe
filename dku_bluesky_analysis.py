import glob
from datetime import datetime
from pytz import timezone
import pandas as pd
from tzlocal import get_localzone
from typing import Optional, List

# Function to read the inventory file
def ebs_read_tbe(flin: str, flsource: str, tblselect: Optional[List[str]] = None):
    """
    Read the inventory file.

    Args:
        flin: Path to the inventory file.
        flsource: Path to the source directory.
        tblselect: List of table names to select.

    Returns:
        A dictionary containing the result and error message (if any).
    """
    result = {}
    error = None

    try:
        tb = pd.read_csv(flin, keep_default_na=False)
        tb_sites = tb.copy()

        if tblselect:
            tb_select = tb_sites[tb_sites['siteid'].isin(tblselect)].reset_index(drop=True)
        else:
            tb_select = tb_sites.copy()

        result['tb'] = tb
        result['tb_sites'] = tb_sites
        result['tb_select'] = tb_select

    except Exception as e:
        error = str(e)

    return {'result': result, 'error': error}

def dks_uread_blueskyv2b():
    """
    Test program to read TSI Bluesky files and create filtered output.
    v2b: read files with single site in subdirectory with serial number.
    TSI version 2, b: directory structure by time and serial number.
    """

    # Clear all variables
    # rm(list=ls()) --> Not necessary in Python

    # Import required libraries
    # library(tidyverse) --> Importing pandas library
    # library(lubridate) --> Importing datetime module from datetime package
    # library(tidyquant) --> Not required in Python
    # library(timetk) --> Not required in Python

    # Define input parameters

    asites = ['npl_bsk_bkt06', 'npl_bsk_amc_brt']
    site_str = f'bsk_ns{len(asites)}'

    asites = ['bgd_3_mohakhali']
    site_str = 'mohakhali'

    asites = ['bgd_43_rajshahi_thakurmara2', 'bgd_44_rajshahi_nowdapara', 'bgd_45_rajshahi_thakurmara', 'bgd_48_rajshahi_u']
    site_str = f'rajshahi_ns{len(asites)}'

    tinterval_str = '15min'

    # timeminsct, timemaxsct: option to screen by time
    # use this to remove data before the instruments were deployed
    timeminsct = None
    timemaxsct = None
    timeminsct = pd.to_datetime('2021-10-01 00:00')
    #timemaxsct = pd.to_datetime('2023-02-15 00:00')

    # Input directory of data
    indir = '../Dku_data_pull/Our Data/Bangladesh/'

    indirsites = ''
    flsites = 'saq_bluesky_npl_20220830_20230404_inv_tbe.csv'
    flsites = 'saq_bluesky_dku_20210715_20230131_inv_tbe.csv'
    flsites = 'saq_bluesky_bgd_20211001_20230430_inv_tbe.csv'

    # Read the inventory file
    rtn = ebs_read_tbe(flin=flsites, flsource=indirsites, tblselect=None)

    if rtn['error'] is None:
        tb = rtn['result']['tb']
        tc = rtn['result']['tc']
        tb_sites = rtn['result']['tb_sites']
        tc_sites = rtn['result']['tc_sites']
    else:
        raise ValueError(f"ebs_read_tbe read error: {rtn['error']}")

    tb_select = tb_sites[tb_sites['siteid'].isin(asites)].reset_index(drop=True)
    aserial = tb_select['serial_number']
    asitenames = tb_select['sitename']
    aflin = []

    for ns in aserial:
        afldata = glob.glob(f'{indir}*/{ns}/Level1.csv')
        aflin.extend(afldata)

    timezone_output = 'Asia/Kathmandu'

    docheckduplicates = 1
    doprintduplicates = 0

    doutc = 1
    docoords = 1

    docutoff = 0
    pm25_cutoff = 500
    pm25_cutoff_value = pd.NA

    doplot = 1
    doraw = 1
    do24hr = 1

    nf = 0
    tb_all = []

    for flin in aflin:
        tf = pd.read_csv(flin)
        tb_step = pd.DataFrame(tf)

        tb_sub = tb_step[tb_step['Site.Name'].isin(asitenames)]

        if tb_sub.empty:
            continue

        tb_sub['date'] = pd.to_datetime(tb_sub['Timestamp..UTC.'], format='%Y-%m-%d %H:%M:%S')
        tb_sub['date'] = tb_sub['date'].dt.tz_localize('UTC').dt.tz_convert(timezone_output)

        tb_sub.rename(columns={'PM2.5..ug.m3.': 'pm25', 'Applied.PM2.5.Custom.Calibration.Factor': 'pm25_scale', 'Site.Name': 'sitename'}, inplace=True)
        tb_sub['sitename'] = tb_sub['sitename'].astype('category')

        print(f"Read {flin}: {len(tb_sub)} rows from {tb_sub['date'].min()} to {tb_sub['date'].max()}")

        if nf == 0:
            tb_all = tb_sub.copy()
        else:
            tb_all = pd.concat([tb_all, tb_sub], ignore_index=True)

        nf += 1

    tb_all.sort_values(by=['sitename', 'date'], inplace=True)
    print(f"Read {nf} files, {len(tb_all)} rows from {tb_all['date'].min()} to {tb_all['date'].max()}")

    if docheckduplicates:
        tb_duplicates = tb_all[tb_all.duplicated(subset=['sitename', 'date'], keep=False)]
        ndup = len(tb_duplicates)

        if ndup > 0:
            print(f"Found {ndup} duplicates")
            if doprintduplicates:
                for i, row in tb_duplicates.iterrows():
                    print(f"Duplicate {i + 1}: {row['date']}, {row['sitename']}")

        tb_all.drop_duplicates(subset=['sitename', 'date'], keep='first', inplace=True)
        print(f"Duplicate check: {len(tb_all)} rows kept")

    tb_all['pm25_v0'] = tb_all['pm25'] / tb_all['pm25_scale']

    for sitesct in asites:
        tbs = tb_all[tb_all['sitename'] == sitesct]
        pm25_factor = tbs['pm25_scale'].dropna().unique()

        if len(pm25_factor) == 0:
            print(f"pm25_scale not found for {sitesct}, do nothing")
        elif len(pm25_factor) == 1:
            tbcount = tbs[tbs['pm25_scale'].isna()].shape[0]

            tb_all.loc[(tb_all['sitename'] == sitesct) & (tb_all['pm25_scale'].isna()), 'pm25'] *= pm25_factor[0]
            tb_all['pm25_scale_calc'] = tb_all['pm25'] / tb_all['pm25_v0']

            print(f"Applied pm25_scale = {pm25_factor[0]} to {tbcount} values from site {sitesct} for which pm25_scale==NA")
        else:
            print(f"Multiple pm25_scale found for {sitesct}, do nothing for now")

    if timeminsct is not None:
        tb_all = tb_all[tb_all['date'] >= timeminsct]
        if len(tb_all) == 0:
            raise ValueError(f"No data found, check data selection in timeminsct: {timeminsct}")
        else:
            print(f"Filtered tb by timeminsct {timeminsct}: {len(tb_all)} rows from {tb_all['date'].min()} to {tb_all['date'].max()}")

    if timemaxsct is not None:
        tb_all = tb_all[tb_all['date'] <= timemaxsct]
        if len(tb_all) == 0:
            raise ValueError(f"No data found, check data selection in timemaxsct: {timemaxsct}")
        else:
            print(f"Filtered tb by timemaxsct {timemaxsct}: {len(tb_all)} rows from {tb_all['date'].min()} to {tb_all['date'].max()}")

    print(f"Using {len(tb_all)} rows from {tb_all['date'].min()} to {tb_all['date'].max()}")

    if docutoff:
        tb_high = tb_all[tb_all['pm25'] > pm25_cutoff]
        tb_all.loc[tb_all['pm25'] > pm25_cutoff, 'pm25'] = pm25_cutoff_value
        print(f"Replaced {len(tb_high)} pm25 values above {pm25_cutoff} with {pm25_cutoff_value}")

    # Plot using timetk
    print("For timetk plot, from RStudio Console: tb %>% group_by(sitename) %>% plot_time_series(date,pm25)")

    tbhr = tb_all.groupby(['sitename', pd.Grouper(key='date', freq='H', closed='left')]).agg({'pm25': 'mean', 'sitename': 'first'}).reset_index()
    tbhr = tbhr.asfreq(freq='H')
    
    if docoords == 1:
        tbhr = pd.merge(tbhr, tb_all.groupby('sitename').last()[['Latitude', 'Longitude']], on='sitename')
        
        if do24hr:
            tb24hr = tb_all.groupby(['sitename', pd.Grouper(key='date', freq='D', closed='left')]).agg({'pm25': 'mean', 'sitename': 'first'}).reset_index()
            tb24hr = tb24hr.asfreq(freq='D')
            tb24hr = pd.merge(tb24hr, tb_all.groupby('sitename').last()[['Latitude', 'Longitude']], on='sitename')

    # Get duration interval
    thr_duration = tbhr.groupby(pd.Grouper(key='date', freq='H')).size().value_counts()
    print("Table of duration for hourly data:")
    print(thr_duration)

    tbhr_valid = tbhr.dropna(subset=['pm25'])
    date_start = tbhr_valid['date'].min().floor('D')
    date_end = tbhr_valid['date'].max().ceil('D')
    nrec = len(tbhr)

    flroot = f"dku_bluesky_{site_str}_{date_start.strftime('%Y%m%d')}_{date_end.strftime('%Y%m%d')}"
    if docoords:
        flroot = f"{flroot}_coords"

    if doutc:
        flcsv = f"{flroot}_hr_utc.csv"
        tbhr.to_csv(fcsv, index=False)
        print(f"Wrote {flcsv}")

    flcsv = f"{flroot}_hr_lt.csv"
    tbhr.to_csv(fcsv, index=False)
    print(f"Wrote {flcsv}")

    if do24hr:
        flcsv = f"{flroot}_24hr_lt.csv"
        tb24hr.to_csv(fcsv, index=False)
        print(f"Wrote {flcsv}")

    if doraw:
        tbout = tb_all[['sitename', 'date', 'pm25_v0', 'pm25', 'pm25_scale_calc', 'pm25_scale']]

        if doutc:
            flcsv = f"{flroot}_{tinterval_str}_utc.csv"
            tbout.to_csv(fcsv, index=False)
            print(f"Wrote {flcsv} with scaled and unscaled pm25")

        flcsv = f"{flroot}_{tinterval_str}_lt.csv"
        tbout.to_csv(fcsv, index=False)
        print(f"Wrote {flcsv} with scaled and unscaled pm25")
