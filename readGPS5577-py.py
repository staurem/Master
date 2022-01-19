# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 08:48:29 2022

@author: juliesi
"""

import glob, os
import pandas as pd
from math import sqrt
import re
import datetime
import func


siteLocs = {'BJN': [74.5038, 19.0012, 0.026],
            'HOP': [76.5089, 25.0144, 0.014],
            'LYR': [78.147, 16.038, 0.522],
            'NYA': [78.923, 11.929, 0.021],
            'HOR': [77.000,15.550,0.010]}

os.chdir("C:/Users/Florine/Desktop/28_10_2019/gps_HOR")#### choose directory from where to read in the txt files
files=glob.glob('*_HOR_REDOBS_gal.txt', recursive=True) ### here I choose the ending I want the file to have, I read in all the ones for galileo here on Hornsund
#### you can just put all the files for multiple months in the same folder and read it in
GPS=pd.read_csv(files[0],sep=',', delimiter=',', header=[12],nrows=0,skipinitialspace=True)
GPS.columns = GPS.columns.str.replace(' ', '')


projAlt=150 ### piercing point alitude https://en.wikipedia.org/wiki/Ionospheric_pierce_point

GPStow_start=datetime(1980,1,6,0,0,0)

for i in range(len(files)):
    GPStemp = pd.read_csv(files[i],sep=',', delimiter=',', header=[12],parse_dates=['HHMM'], skipinitialspace=True)
    week=pd.read_csv(files[i],delimiter=' ', header=None, skiprows = 16, nrows=1, skipinitialspace=True)
    week.replace(',','', regex=True, inplace=True)
    GPStemp.columns = GPStemp.columns.str.replace(' ', '')

    GPStemp['week']=int(week.loc[0,2])
    GPStemp['SatSys']=week.loc[0,5]
    DateDay=re.findall(r'\d+', files[i])[0]
    GPStemp['TOWDate']=GPStow_start+pd.to_timedelta(GPStemp.week*7, unit='d')+pd.to_timedelta(GPStemp.GPSTOW, unit='s')
    cordi=pd.DataFrame({'long': [],'lat': []})
    for k in range(len(GPStemp)):
        coords=func.cnv_azel2latlon(GPStemp['Az'][k], GPStemp['Elv'][k], projAlt,siteLocs['HOR']) ### just a function converting Azimuth and Elevation and Altitude to latitude and longitude
        cordi=cordi.append({'lat':coords[0], 'long': coords[1]},ignore_index=True)  
    GPStemp=GPStemp.assign(**{'long': [*cordi.long], 'lat': [*cordi.lat]})
    GPS=pd.concat([GPS,GPStemp])
GPS=GPS.reset_index(drop=True)


GPS.to_pickle('GAL_HOR_28-10_green.pkl') #### name the file you want to save