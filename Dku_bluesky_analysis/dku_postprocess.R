## dku_postprocess.R: Test program to plot time variation of Dhaka University data
## Execute in RStudio using: source('dku_postprocess.R')
##
## 9 May 2023

rm(list=ls())
library(tidyverse)
library(lubridate)
library(openair)
#library(plotly) # use ggplotly(p) for interactive plot

## we need printf from bdf_utils.R:
source('bdf_utils.R')

varsct = 'pm25'
varunits = 'ug/m3'

## for 2 seasons, Dry or Wet, use this:
seasonsct = 'Dry' # NULL, 'Dry', 'Wet'
tb_season <- tibble(name=c('Dry','Wet','Dry'),start_mmdd=c(1,401,1101))

## for 3 seasons, use this:
#seasonsct = NULL # NULL, 'Cool', 'Hot', 'Monsoon'
#tb_season <- tibble(name=c('Cool','Hot','Monsoon','Cool'),start_mmdd=c(1,301,601,1101))

## for 4 seasons, use this:
#seasonsct = NULL # NULL, 'Winter', ...
#tb_season <- tibble(name=c('Winter','PreMonsoon','Monsoon','PostMonsoon','Winter'),
#                    start_mmdd=c(1,301,601,901,1201))

## timeminsct, timemaxsct: option to screen by time
## use this to remove data before the insruments were deployed
## NULL: no screening
timeminsct <- NULL
timemaxsct <- NULL
#timeminsct <- ymd_hm('2022-07-01 00:00')
#timemaxsct <- ymd_hm('2023-01-01 00:00')

timezone_output = 'Asia/Dhaka'

## There are 2 types of files:
##  ftype == 1: UTC files with dates in R format
##  ftype == 2: Local Time files with dates in Excel format

## Input directory and file name: indir, flroot
indir = ''
#flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_utc'; ftype = 1
#flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_lt'; ftype = 2
flroot = 'dku_bluesky_rajshahi_ns4_20220421_20230202_coords_hr_lt'; ftype = 2
flroot = 'dku_bluesky_rajshahi_ns4_20220421_20230501_coords_hr_lt'; ftype = 2

flin = sprintf('%s%s.csv',indir,flroot)
flrootout = sprintf('p%s',flroot)

count_min = 3 # NULL: no check, >0: minimum number of observations required per hour

domatch = 1 # 1: do only times with valid data for all sites

doallsites = 0 # 0: skip plots; 1: timevariation plot for each site one by one
doallseasons = 1 # 0: skip plots; 1: timevariation plot for each season one by one

dowritecsv = 0 # 1: output csv file with tibble actually used for plotting

## size of png graphics to save to file
fgwidth = 1000; fgheight = 800

## read data:
tb <- read_csv(flin)

## set time zone:
if ( ftype == 1 ) {
    tb$date <- with_tz(tb$date,timezone_output) # for files in UTC, shift to local
} else {
    tb$date <- force_tz(tb$date,timezone_output) # for files in local, force local
    tb <- tb %>% select(-'...1')
}

printf('Read %d rows from %s to %s',nrow(tb),min(tb$date),max(tb$date))

## create column with seasons:
tb$season0 <- base::cut(100*month(tb$date)+day(tb$date),
                        breaks=c(tb_season$start_mmdd-1,1231),
                        labels=tb_season$name)

## create time of day categories for plotting:
tb$timeofday = c('Night','Trans','Day','Trans','Night')[cut(hour(tb$date),c(-1,8.5,10.5,16.5,18.5,24))]
tb$timeofday = as.factor(tb$timeofday)

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

## filter data by season if required:
if ( !is.null(seasonsct) ) {
    tb <- tb %>% filter(season0==seasonsct)
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data found, check data selection in seasonsct: %s',seasonsct),call.=FALSE)
    } else {
        printf('Filtered tb by season %s: %d rows from %s to %s',seasonsct,nrow(tb),min(tb$date),max(tb$date))
    }
}

if ( !is.null(count_min) ) {
    tb <- tb %>% filter(pm25count>=count_min)
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data left after screening for pm25count >= %d (count_min)',count_min),call.=FALSE)
    } else {
        printf('Filtered tb by pm25count >= %d (count_min), %d rows from %s to %s',count_min,nrow(tb),min(tb$date),max(tb$date))
    }
}

## Matching data: do only times which have valid data for all sites
if ( domatch ) {
    ## tb_wide has one column of pm25 per site, side by side:
    tb_wide <- tb %>%
        select(date,sitename,pm25) %>%
        pivot_wider(names_from=sitename,values_from=pm25)

    ## we keep only the rows with data for all sites:
    nrow_all = nrow(tb_wide)
    asites = unique(tb$sitename)
    tb_wide <- tb_wide %>% drop_na(all_of(asites))
    nrow_allvalid = nrow(tb_wide)
    printf("%d/%d rows with valid data for all sites",nrow_allvalid,nrow_all)
    if ( nrow_allvalid == 0 ) {
        stop(sprintf('No valid data found, stop here'),call.=FALSE)
    }

    ## we now filter the original data with the times for which we have complete data:
    tb <- tb %>% filter(date %in% tb_wide$date)

    if ( dowritecsv ) {
        ## To check what is in tb_wide, write to csv and look in Excel:
        flcsv <- sprintf('%s_postprocess_wide.csv',flrootout)
        write.csv(tb_wide,flcsv)
        printf('Wrote data with one column per site (tb_wide) to %s for QAQC',flcsv)
    }
}

## Date string for plot titles:
date_str = sprintf('%s to %s',date(min(tb$date)),date(max(tb$date)))
date_str_flname = sprintf('%s_%s',format(min(tb$date),'%Y%m%d'),format(max(tb$date),'%Y%m%d'))
if  ( !is.null(seasonsct) ) {
    date_str = sprintf('%s (%s)',date_str_flname,seasonsct)
    date_str_flname = sprintf('%s_%s',date_str_flname,tolower(seasonsct))
}

## Summary time series, histogram and metrics:
summaryPlot(tb%>%rename(site=sitename),pollutant='pm25')
flout = sprintf("%s_summary.png",flrootout)
dev.copy(png, flout, width=fgwidth, height=fgheight)
dev.off()
printf('Summary plot created: %s',flout)

## Plot time series:
plts = ggplot(tb) +
    geom_line(aes(x=date,y=pm25,color=sitename))
show(plts)

## Interactive plotting, do ggplotly(plts) in the RStudio Console
printf('For interactive plotting, type in the RStudio Console: ggplotly(plts)')
printf('Note: you will probably first need to type: library(plotly)')

## Plot temporal variations by day, week, month: overlay sites:
## statistic: can be 'mean' or 'median', see openair manual
ptv <- timeVariation(tb, pollutant=varsct,
                     group='sitename', normalise=FALSE,
                     key.columns = 2, statistic = 'median', conf.int = c(0.75),
                     main=sprintf('%s (%s) by site\n%s', varsct, varunits, date_str))

if ( doallsites ) {
    ## Temporal variation: one figure per site, overlay seasons:
    ## use filter to plot one site at a time
    asites = unique(tb$sitename)
    for ( sitesct in asites ) {
        siteid = saq_sitename2id(sitesct)
        ## Plot temporal variations by day, week, month:
        ptv <- timeVariation(filter(tb,sitename==sitesct), pollutant=varsct,
                             group='season0', normalise=FALSE,
                             main=sprintf('%s (%s) for site %s\n%s', varsct, varunits, sitesct, date_str))

        flout = sprintf("%s_tvsite_%s.png",flrootout,siteid)
        dev.copy(png, flout, width=fgwidth, height=fgheight)
        dev.off()
        printf('Time Variation plot created: %s',flout)
    }
}

if ( doallseasons ) {
    ## Temporal variation: one figure per season, overlay sites:
    ## use filter to plot one season at a time
    aseasons = unique(tb$season0)
    for ( seasonsct in aseasons ) {
        ## Plot temporal variations by day, week, month:
        ptv <- timeVariation(filter(tb,season0==seasonsct), pollutant=varsct,
                             group='sitename', normalise=FALSE,
                             main=sprintf('%s (%s) for season %s\n%s', varsct, varunits, seasonsct, date_str))

        flout = tolower(sprintf("%s_tvseason_%s.png",flrootout,seasonsct))
        dev.copy(png, flout, width=fgwidth, height=fgheight)
        dev.off()
        printf('Time Variation plot created: %s',flout)
    }
}

if ( dowritecsv ) {
    ## use write.csv to have Excel dates:
    ## in local time (timezone_output):
    flcsv <- sprintf('%s_postprocess_qa.csv',flrootout)
    write.csv(tb,flcsv)
    printf('Wrote data tibble (tb) to %s for QAQC',flcsv)
}
