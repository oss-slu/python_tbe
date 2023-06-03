## Plot map using inventory data in TBE csv file
## Colorscale: number of data records (see nrecords below)
##
## Benjamin de Foy, 2 May 2023

rm(list=ls())

library(tidyverse)
library(openair)
library(gridExtra)
library(GGally)
library(ggpmisc)
library(leaflet)
library(pals)

## For saving map to html/png:
## Make sure you have installed phantomjs from the command-line:
## webshot::install_phantomjs() # installed phantomjs to /home/bdf/bin
library(webshot2)
library(htmlwidgets)
##library(mapview) ## mapshot does not work as well as webshot for png, but it creates a standalone html file

## We need function ebs_read_tbe.R to read the inventory file:
source('ebs_read_tbe.R')
source('bdf_utils.R')

indir = ''
flroot = 'saq_bluesky_dku_20210715_20230131_inv'
flroot = 'saq_bluesky_npl_20220830_20230404_inv'
flroot = 'saq_bluesky_bgd_20211001_20230430_inv'

flrootout = sprintf('p%s',flroot)

flin = sprintf('%s_tbe.csv',flroot)

sites_str = 'bgd'

ndata_min_summary = 100

domap = 1
dlatlon = 0.01
cmin_ref = 0 # if NULL, use min(data)
cmax_ref = 220 # if NULL, use max(data)
cmax_ref = NULL; cmin_ref = NULL

plot2file = 1 # save to html (zoomable), to png if dowebshot == 1
dowebshot = 1 # creating png requires chrome
## Set margins:
##par(mar=c(0,0,0,0)+1.5)
ggwidth = 25
ggheight = 20
ggdpi = 100

rtn <- ebs_read_tbe(flin=flin, flsource=indir, tblselect=NULL)
if ( is.null(rtn$error) ) {
    tb <- rtn$result$tb
    tc <- rtn$result$tc
    tb_sites <- rtn$result$tb_sites
    tc_sites <- rtn$result$tc_sites
} else {
    stop(rtn$error,call.=FALSE)
    #return( list(result=NULL, error=sprintf('tbe_map_inventory.R read error from ebs_read_tbe: %s',rtn$error)) )
}

tb_sites$siteid = as.factor(tb_sites$siteid)
tbsct = tb_sites

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

    cmin_data = floor(min(tbsct$nrecords))
    cmax_data = ceiling(max(tbsct$nrecords))
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
    lgd_str = sprintf('NRecords')

    pmap = leaflet(tbsct) %>% addTiles() %>%
        addCircleMarkers(lng = ~longitude, lat = ~latitude,
                         radius = 10, weight = 2, stroke = TRUE,
                         fillOpacity = 0.8,
                         label= ~as.character(nrecords),
                         popup = ~as.character(sitename),
                         color = 'black',
                         fillColor = ~pal(nrecords)) %>%
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
        flhtml = tolower(sprintf('%s_map.html',flrootout))
        saveWidget(pmap,flhtml,selfcontained=FALSE)
        printf('You can open %s in a web browser to view the figure interactively',flhtml)
        if ( dowebshot ) {
          flout = tolower(sprintf('%s_map.png',flrootout))
          webshot(flhtml,file=flout,cliprect='viewport')
          printf('Figure saved to %s',flout)
        }
    }
}

printf('Type show(pmap) in the console to show the map')
