## dku_read_bluesky.R: Test program to read TSI Bluesky files and create filtered output
## Execute in RStudio using: source('dku_read_bluesky.R')
##
## 13 Mar 2023

rm(list=ls())
library(tidyverse)
library(lubridate)
## Use timetk to do time averages - more robust than timeAverage from OpenAir
library(tidyquant)
library(timetk)

## we need printf from bdf_utils.R:
source('bdf_utils.R')

## Modify asites and site_str below to retrieve the sites that you want:
## asites contains the sites you want to extract
## site_str is a short description of the sites for use in the output filename

asites = c('65. Sylhet MPU','66. Sylhet Ambarkhana')
site_str = sprintf('sylhet_ns%d',length(asites))

asites = c('Dhaka University 75','74. CARS','62. Curzon hall','40. Anondo Bazar')
site_str = sprintf('dku_ns%d',length(asites))

asites = c('1. Siddeshwari','2. Dhaka University','3. Mohakhali')
site_str = sprintf('dhaka_ns%d',length(asites))

asites = c('43. Rajshahi Thakurmara2','44. Rajshahi Nowdapara','45. Rajshahi Thakurmara','48. Rajshahi University')
site_str = sprintf('rajshahi_ns%d',length(asites))

## timeminsct, timemaxsct: option to screen by time
## use this to remove data before the insruments were deployed
## NULL: no screening
timeminsct <- NULL
timemaxsct <- NULL
timeminsct <- ymd_hm('2021-10-01 00:00')
#timemaxsct <- ymd_hm('2023-02-15 00:00')

## Input directory of data:
#indir = 'D:/cloud data for meeting/'
#indir = 'C:/Users/bdefoy/Desktop/Dku_cloud_data/'
indir = '../Dku_cloud_data/'

## List of files to read in aflin:
aflin = c('11. July to dec 21 min',
          '12. Jan to April 22 min',
          '13. May to July 22 min',
          '14. Aug to Sep 22 min',
          '15. Oct 22 to Jan 23 min')

## For testing, try just 2 files:
#aflin = c('11. July to dec 21 min',
#          '12. Jan to April 22 min')

timezone_output = 'Asia/Dhaka'

docheckduplicates = 1 # 1: remove duplicate times using distinct
doprintduplicates = 0 # 1: print duplicate times to screen

doutc = 0 # 1: output csv files in UTC time in R format
docoords = 1 # 1: include lat/lon in output file for mapping

## docutoff == 1: replace values above cutoff with NA
docutoff = 1
pm25_cutoff = 500
pm25_cutoff_value = NA

doplot = 1 # 1: make time series plot for QA
do15min = 1 # 1: output data at original resolution
do24hr = 1 # 1: calculate 24-hour averages

nf = 0
## Loop over input files and combine data into "tb"
for ( flin in aflin ) {
    flcsv_full = sprintf('%s%s.csv',indir,flin)

    tf <- read.csv(flcsv_full, header=TRUE, sep=",")
    tb_step = tibble(tf)

    tb_sub <- tb_step %>% filter(Site.Name %in% asites)

    ## if there is no data, skip to next file
    if ( nrow(tb_sub) == 0 ) {
        next
    }

    date <- as.POSIXct(mdy_hm(tb_sub$Timestamp..UTC.),format="%Y-%m-%d %H:%M:%S")
    date <- with_tz(date,timezone_output)

    tb_sub$date = date
    tb_sub <- tb_sub %>% rename(pm25='PM2.5..ug.m3.')
    tb_sub <- tb_sub %>% rename(pm25_scale='Applied.PM2.5.Custom.Calibration.Factor')
    tb_sub <- tb_sub %>% rename(sitename='Site.Name')
    tb_sub$sitename <- as.factor(tb_sub$sitename)

    printf('Read %s: %d rows from %s to %s',flin,nrow(tb_sub),min(tb_sub$date),max(tb_sub$date))

    if ( nf == 0 ) {
        tb <- tb_sub
    } else {
        tb <- bind_rows(tb,tb_sub)
    }
    nf = nf + 1
}

## sort data:
tb <- tb %>% arrange(sitename,date)

printf('Read %d files, %d rows from %s to %s',nf,nrow(tb),min(tb$date),max(tb$date))

## check for duplicate dates
## (code from ebs_duplicate_dates.R)
if ( docheckduplicates ) {
    nrow1 = nrow(tb)
    for ( sitesct in unique(tb$sitename) ) {
        tbs <- tb %>% filter(sitename==sitesct)
        tb_duplicates <- which(duplicated(tbs$date))
        ndup <- length(tb_duplicates)
        if ( ndup > 0 ) {
            printf('Found %d duplicates for site %s\n',ndup,sitesct)
            if ( doprintduplicates ) {
                for ( nd in 1:ndup ) {
                    printf('Duplicate %d: %s, %s\n',nd,tbs$date[tb_duplicates[nd]],sitesct)
                }
            }
        }
    }
    tb <- tb %>% distinct(sitename,date,.keep_all=TRUE)
    nrow2 = nrow(tb)
    printf('Duplicate check: %d/%d rows kept',nrow2,nrow1)
}

## Apply scale factor
## TSI does not apply scale factors retroactively
## If we find a scale factor for a site, we apply it to all the times when the scale factor was NA
## If we find more than one scale factor, we do nothing for now: need to code when situation arises

# Calculate unscaled pm25:
fscale = replace(tb$pm25_scale,is.na(tb$pm25_scale),1)
tb$pm25_v0 = tb$pm25/fscale

# Calculate scaled pm25:
for ( sitesct in asites ) {
    tbs <- tb %>% filter(sitename == sitesct)
    pm25_factor = unique(na.omit(tbs$pm25_scale))
    if ( length(pm25_factor) == 0 ) {
        printf('pm25_scale not found for %s, do nothing',sitesct)
    } else if ( length(pm25_factor) == 1 ) {
        tbcount = tb %>% summarise(count=sum(sitename==sitesct & is.na(pm25_scale)))

        tb <- tb %>% mutate(pm25=ifelse((sitename==sitesct & is.na(pm25_scale)),pm25*pm25_factor,pm25))

        tb$pm25_scale_calc = tb$pm25 / tb$pm25_v0 # for checking

        printf('Applied pm25_scale = %g to %d values from site %s for which pm25_scale==NA',pm25_factor,tbcount$count,sitesct)
    } else {
        printf('Multiple pm25_scale found for %s, do nothing for now: add code if you want to apply pm25_scale to different records',sitesct)
    }
}

## filter data by start/end time if required:
## do this after scaling so we can use scale factors outside of time range if available
if ( !is.null(timeminsct) ) {
  tb <- filter(tb, (tb$date >= timeminsct) )
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data found, check data selection in timeminsct: %s',timeminsct),call.=FALSE)
    } else {
        printf('Filtered tb by timeminsct %s: %d rows from %s to %s',timeminsct,nrow(tb),min(tb$date),max(tb$date))
    }
}
if ( !is.null(timemaxsct) ) {
  tb <- filter(tb, (tb$date <= timemaxsct) )
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data found, check data selection in timemaxsct: %s',timemaxsct),call.=FALSE)
    } else {
        printf('Filtered tb by timemaxsct %s: %d rows from %s to %s',timemaxsct,nrow(tb),min(tb$date),max(tb$date))
    }
}

printf('Using %d rows from %s to %s',nrow(tb),min(tb$date),max(tb$date))

if ( docutoff ) {
    ## reset values above cutoff to NA:
    tb_high <- tb %>% filter(pm25>pm25_cutoff)
    tb <- tb %>%  mutate(pm25=replace(pm25,pm25>pm25_cutoff,pm25_cutoff_value))
    printf('Replaced %d pm25 values above %d with %d',nrow(tb_high),pm25_cutoff,pm25_cutoff_value)
}

## timetk plot: this needs to be done from the command line, and shows up in the viewer, or source using echo=TRUE
printf('For timetk plot, from RStudio Console: tb %%>%% group_by(sitename) %%>%% plot_time_series(date,pm25)')

## get hourly averages with timetk:
if ( docoords == 0 ) {
    ## just sitename, average pm25 and count of pm25 values
    tbhr <- tb %>%
        group_by(sitename) %>%
        summarise_by_time(date,.by='hour',.type='ceiling',
                          pm25count=COUNT(pm25),
                          pm25=mean(pm25),
                          sitename=first(sitename)) %>%
        pad_by_time(date,.by='hour',.pad_value=NA)
} else {
    ## include latitude and longitude in output file:
    tbhr <- tb %>%
        group_by(sitename) %>%
        summarise_by_time(date,.by='hour',.type='ceiling',
                          pm25count=COUNT(pm25),
                          pm25=mean(pm25),
                          sitename=first(sitename),
                          latitude=last(Latitude),
                          longitude=last(Longitude)) %>%
        pad_by_time(date,.by='hour',.pad_value=NA)

    if ( do24hr ) {
        ## calculate 24-hour average:
        tb24hr <- tb %>%
            group_by(sitename) %>%
            summarise_by_time(date,.by='day',.type='ceiling',
                              pm25count=COUNT(pm25),
                              pm25=mean(pm25),
                              sitename=first(sitename),
                              latitude=last(Latitude),
                              longitude=last(Longitude)) %>%
            pad_by_time(date,.by='day',.pad_value=NA)
    }
}

## Get duration interval:
thr_duration <- table(int_length(int_diff(tbhr$date)))
#printf('Table of duration for hourly data:')
#print(thr_duration)

## remove missing data to get correct range
tbhr_valid <- drop_na(tbhr,all_of('pm25'))
## get starting and ending day:
date_start = floor_date(min(tbhr_valid$date),unit='day')
date_end = ceiling_date(max(tbhr_valid$date),unit='day')
nrec <- nrow(tbhr)

## create output filename:
flroot <- sprintf('dku_bluesky_%s_%s_%s',site_str,format(date_start,'%Y%m%d'),format(date_end,'%Y%m%d'))
if ( docoords ) { flroot <- sprintf('%s_coords',flroot) }

## QA plot to make sure we have sensible data:
if ( doplot ) {
    plts = ggplot(tbhr) +
        geom_line(aes(x=date,y=pm25,color=sitename))
    show(plts)
}

if ( doutc ) {
    ## write_csv date format is not compatible with Excel
    ## UTC time zone:
    flcsv <- sprintf('%s_hr_utc.csv',flroot)
    write_csv(tbhr,flcsv,append=FALSE,col_names=TRUE)
    printf('Wrote %s',flcsv)
}

## use write.csv to have Excel dates:
## in local time (timezone_output):
flcsv <- sprintf('%s_hr_lt.csv',flroot)
write.csv(tbhr,flcsv)
printf('Wrote %s',flcsv)

if ( do24hr ) {
    ## use write.csv to have Excel dates:
    ## in local time (timezone_output):
    flcsv <- sprintf('%s_24hr_lt.csv',flroot)
    write.csv(tb24hr,flcsv)
    printf('Wrote %s',flcsv)
}

## Output data at original time resolution:
if ( do15min ) {
    ## Get duration interval for QA:
    t_duration <- table(int_length(int_diff(tb$date)))
    #printf('Table of duration for 15min data:')
    #print(t_duration)

    ## Select data for output file:
    tbout <- tb %>% select(any_of(c('sitename','date','pm25_v0','pm25','pm25_scale_calc','pm25_scale')))

    if ( doutc ) {
        ## write_csv date format is not compatible with Excel
        ## UTC time zone:
        flcsv <- sprintf('%s_15min_utc.csv',flroot)
        write_csv(tbout,flcsv,append=FALSE,col_names=TRUE)
        printf('Wrote %s with scaled and unscaled pm25',flcsv)
    }

    ## use write.csv to have Excel dates:
    ## in local time (timezone_output):
    flcsv <- sprintf('%s_15min_lt.csv',flroot)
    write.csv(tbout,flcsv)
    printf('Wrote %s with scaled and unscaled pm25',flcsv)
}
