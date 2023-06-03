## dku_correlogram.R: Test program to plot time variation of Dhaka University data
##
## 13 Mar 2023

rm(list=ls())
library(tidyverse)
library(lubridate)
library(GGally)
library(ggpmisc)
#library(ggpubr)

## we need printf from bdf_utils.R:
source('bdf_utils.R')

## Variable to plot (sct means select):
varsct = 'pm25'
varunits = 'ug/m3'

## Filter data by season:
seasonsct = NULL # NULL, 'Dry', 'Wet'

timezone_output = 'Asia/Dhaka'

## Input directory and file name: indir, flroot
#indir = 'D:/cloud data for meeting/'
#indir = 'C:/Users/bdefoy/Desktop/Dku_cloud_data/'
indir = ''

#flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_utc'; ftype = 1
flroot = 'dku_bluesky_sylhet_ns2_20220421_20230202_coords_hr_lt'; ftype = 2

flin = sprintf('%s%s.csv',indir,flroot)
flrootout = sprintf('p%s',flroot)

## read the data:
tb <- read_csv(flin)
##asites = c('65. Sylhet MPU','66. Sylhet Ambarkhana')
asites = unique(tb$sitename)

tb$sitename = as.factor(tb$sitename)

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

printf('Found %d rows from %s to %s',nrow(tb),min(tb$date),max(tb$date))

## Date string for plot titles:
date_str = sprintf('%s to %s',date(min(tb$date)),date(max(tb$date)))
date_str_flname = sprintf('%s_%s',format(min(tb$date),'%Y%m%d'),format(max(tb$date),'%Y%m%d'))
if  ( !is.null(seasonsct) ) {
    date_str = sprintf('%s (%s)',date_str_flname,seasonsct)
    date_str_flname = sprintf('%s_%s',date_str_flname,tolower(seasonsct))
}

## Correlogram code wants matching data in separate columns
## For this, we use pivot_wider
## Please check that pivot_wider has done what you expect by writing it to a csv file and inspecting it in Excel

tbs <- tb %>% select(date,sitename,pm25,timeofday,season0)
tb_wide <- tbs %>%
    pivot_wider(names_from=sitename,values_from=pm25)

## Check data availability:
nrow_all = nrow(tb_wide)
tb_wide <- tb_wide %>% drop_na(all_of(asites))
nrow_allvalid = nrow(tb_wide)
printf("%d/%d rows with valid data for all sites",nrow_allvalid,nrow_all)
if ( nrow_allvalid == 0 ) {
    stop(sprintf('No valid data found, stop here'),call.=FALSE)
}

## To check what is in tb_wide, write to csv and look in Excel:
##write.csv(tb_wide, 'test.csv')

## Make correlogram with GGAlly:
p_corr <- ggpairs(tb_wide,columns=asites,
                  ggplot2::aes(colour=timeofday,alpha=0.4),
		  lower=list(continuous='smooth'))

## add x=y lines:
for ( i in 2:p_corr$nrow ) {
  for ( j in 1:(i-1) ) {
    p_corr[i,j] = p_corr[i,j] + geom_abline(intercept=0,slope=1)
  }
}
show(p_corr)
ggsave(sprintf("%s_corr.png",flrootout),width=16,height=16,units="cm",dpi=200)
printf('Correlogram saved to file %s_corr.png',flrootout)

## ggscatter from ggpubr package:
#p_ggsclgd <- ggscatter(tb_wide,x=asites[1],y=asites[2],
#                       color='timeofday',shape='timeofday',
#                       add='reg.line',conf.int=TRUE )+
#    stat_cor(aes(color=timeofday),label.x=4)+
#    ggtitle(sprintf('CC %s, %s',asites[1],asites[2]))
#show(p_ggsclgd)

## Correlation plot using ggpmisc to write equation on figure:
p_xy <- ggplot(data=tb_wide, aes(x=.data[[asites[1]]],
                                 y=.data[[asites[2]]],
                                 colour = timeofday)) +
    stat_poly_line() +
    stat_poly_eq(aes(label=paste(after_stat(eq.label),
                                 after_stat(rr.label),
                                 sep="*\", \"*"))) +
    geom_point()

show(p_xy)
ggsave(sprintf("%s_xy.png",flrootout),width=12,height=12,units="cm",dpi=200)
printf('XY plot saved to file %s_xy.png',flrootout)
