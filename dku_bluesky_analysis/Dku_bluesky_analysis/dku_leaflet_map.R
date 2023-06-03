## dku_leaflet_map.R: Test program to map TSI Bluesky data
##
## 13 Mar 2023

rm(list=ls())
library(tidyverse)
library(lubridate)
library(leaflet)
library(pals)

## For saving map to html/png:
## Make sure you have installed phantomjs from the command-line:
## webshot::install_phantomjs() # installed phantomjs to /home/bdf/bin
library(webshot2)
library(htmlwidgets)
##library(mapview) ## mapshot does not work as well as webshot for png, but it creates a standalone html file

## we need printf and addLegend_decreasing from bdf_utils.R:
source('bdf_utils.R')

## Variable to plot (sct means select):
varsct = 'pm25'
varunits = 'ug/m3'

## Filter data by date/time:
## Season, time of day and min/max time to select.
## Use NULL if you do not want to filter
seasonsct = 'Dry' # NULL, 'Dry', 'Wet'
timeofdaysct = 'Night' # NULL, 'Day', 'Night', 'Trans'
timeminsct <- NULL
timemaxsct <- NULL
#timeminsct <- ymd_hm('2022-12-15 00:00')
#timemaxsct <- ymd_hm('2023-02-15 00:00')

timezone_output = 'Asia/Dhaka'

## Input directory and file name: indir, flroot
indir = ''
#flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_utc'; ftype = 1
flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_lt'; ftype = 2

flin = sprintf('%s%s.csv',indir,flroot)
flrootout = sprintf('p%s',flroot)

domap = 1
dlatlon = 0.01
##cmin_ref = 0 # if NULL, use min(data)
##cmax_ref = 220 # if NULL, use max(data)
cmax_ref = NULL; cmin_ref = NULL

## size of png graphics to save to file
fgwidth = 800; fgheight = 700
plot2file = 1 ## 1: save figure to html and png files

## read the data:
tb <- read_csv(flin)

if ( ftype == 1 ) {
    tb$date <- with_tz(tb$date,timezone_output) # for files in UTC, shift to local
} else {
    tb$date <- force_tz(tb$date,timezone_output) # for files in local, force local
    tb <- tb %>% select(-'...1')
}

printf('Read %d rows from %s to %s',nrow(tb),min(tb$date),max(tb$date))

## create vector of seasons for filtering:
tb_season <- tibble(name=c('Dry','Wet','Dry'),start_mmdd=c(1,401,1101))
tb$season0 <- base::cut(100*month(tb$date)+day(tb$date),
                        breaks=c(tb_season$start_mmdd-1,1231),
                        labels=tb_season$name)

## create time of day categories for plotting:
tb$timeofday = c('Night','Trans','Day','Trans','Night')[cut(hour(tb$date),c(-1,8.5,10.5,16.5,18.5,24))]
tb$timeofday = as.factor(tb$timeofday)

## filter data by season if required:
if ( !is.null(seasonsct) ) {
    tb <- tb %>% filter(season0==seasonsct)
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data found, check data selection in seasonsct: %s',seasonsct),call.=FALSE)
    } else {
        printf('Filtered tb by season %s: %d rows from %s to %s',seasonsct,nrow(tb),min(tb$date),max(tb$date))
    }
}

## filter data by time of day if required:
if ( !is.null(timeofdaysct) ) {
    tb <- tb %>% filter(timeofday==timeofdaysct)
    if ( nrow(tb) == 0 ) {
        stop(sprintf('No data found, check data selection in timeofdaysct: %s',timeofdaysct),call.=FALSE)
    } else {
        printf('Filtered tb by time of day %s: %d rows from %s to %s',timeofdaysct,nrow(tb),min(tb$date),max(tb$date))
    }
}

## filter data by start/end time if required:
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

printf('Found %d rows from %s to %s',nrow(tb),min(tb$date),max(tb$date))

## Date string for plot titles:
date_str = sprintf('%s to %s',date(min(tb$date)),date(max(tb$date)))
date_str_flname = sprintf('%s_%s',format(min(tb$date),'%Y%m%d'),format(max(tb$date),'%Y%m%d'))
if  ( !is.null(seasonsct) ) {
    date_str = sprintf('%s (%s)',date_str_flname,seasonsct)
    date_str_flname = sprintf('%s_%s',date_str_flname,tolower(seasonsct))
}


## get mean and count by site and season:
tbsct <- tb %>%
    group_by(sitename) %>%
    summarise(pm25_mean=mean(pm25,na.rm=TRUE),
              pm25_stdev=sqrt(var(pm25,na.rm=TRUE)),
              pm25_count=sum(!is.na(pm25)),
              latitude=mean(latitude,na.rm=TRUE),
              longitude=mean(longitude,na.rm=TRUE))

tbsct <- tbsct %>%
    mutate(pm25_mean = round(pm25_mean, digits = 1)) %>%
    mutate(pm25_stdev = round(pm25_stdev, digits = 1))

if ( domap ) {
    latmin = min(tbsct$latitude); latmax = max(tbsct$latitude)
    lonmin = min(tbsct$longitude); lonmax = max(tbsct$longitude)
    lat1 = latmin - dlatlon
    lat2 = latmax + dlatlon
    lon1 = lonmin - dlatlon
    lon2 = lonmax + dlatlon
    ##dlatlon = max(latmax-latmin,lonmax-lonmin)
    ##lat0 = mean(c(latmin,latmax)); lon0 = mean(c(lonmin,lonmax))
    ##lat1 = lat0-dlatlon*.5; lat2 = lat0+dlatlon*.5
    ##lon1 = lon0-dlatlon*.5; lon2 = lon0+dlatlon*.5

    cmin_data = floor(min(tbsct$pm25_mean))
    cmax_data = ceiling(max(tbsct$pm25_mean))
    printf('Data Range: %f to %f',cmin_data,cmax_data)
    if ( is.null(cmin_ref) ) {
        cmin_lgd = cmin_data
    } else {
        cmin_lgd = cmin_ref
    }
    if ( is.null(cmax_ref) ) {
        cmax_lgd = cmax_data
    } else {
        cmax_lgd = cmax_ref
    }

    cmap = kovesi.rainbow(10)
    pal = colorNumeric(palette=cmap,domain=c(cmin_lgd,cmax_lgd))
    ## \U003BC == mu; \U00B3 == superscript 3; \U2083 == subscript 3
    lgd_str = sprintf('PM2.5 Conc </br> (\U003BCg / m\U00B3) </br>')

    pmap = leaflet(tbsct) %>% addTiles() %>%
        addCircleMarkers(lng = ~longitude, lat = ~latitude,
                         radius = 10, weight = 2, stroke = TRUE,
                         fillOpacity = 0.8,
                         label= ~as.character(pm25_mean),
                         popup = ~as.character(sitename),
                         color = 'black',
                         fillColor = ~pal(pm25_mean)) %>%
        addLegend_decreasing("topright",title=lgd_str,pal=pal,values=c(cmin_lgd,cmax_lgd),opacity=1,decreasing=TRUE) %>%
        fitBounds(lon1,lat1,lon2,lat2)

    if ( plot2file ) {
        ## mapshot does not work as well as webshot for png:
        ##flout = tolower(sprintf('%s_mapshot.png',flrootout))
        ##mapshot(pmap,url='toto_mapshot.html',file=flout)
        ## mapshot creates stand-alone html file:
        ##flhtml = tolower(sprintf('%s_mapshot.html',flrootout))
        ##mapshot(pmap,url=flhtml)

        ## webshot creates html with subdirectory and then creates png image
        flout = tolower(sprintf('%s_map_pm25.png',flrootout))
        flhtml = tolower(sprintf('%s_map_pm25.html',flrootout))
        saveWidget(pmap,flhtml,selfcontained=FALSE)
        webshot(flhtml,file=flout,cliprect='viewport')
        printf('You can open %s in a web browser to view the figure interactively',flhtml)
    }
}

printf('Type show(pmap) in the console to show the map')
