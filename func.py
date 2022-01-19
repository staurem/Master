# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 08:47:40 2022

@author: juliesi
"""

import numpy as np 
import math
from math import radians, degrees, cos, sin, tan, sqrt, atan, atan2, floor, pi, asin, trunc, modf,acos
def cnv_azel2latlon(az, el, ht, site):
# %
# % Function to convert from an azimuth/elevation grid to a
# % latitude/longitude grid given an unwarping height and a site location.
# % For elevations below the horizon, returns NaN.
# %
# % INPUTS:
# %   az - M x N array of azimuths to be converted [degrees]
# %   el - M x N array of elevation to be converted [degrees]
# %   ht - M x N array of heights to be used in the conversion [km]
# %   site - 1 x 2 array containing [latitude, longitude] of the site
# %          [degrees]
# %
# % OUTPUTS:
# %   lat - M x N array of latitudes [degrees]
# %   lon - M x N array of longitudes [degrees]
# %
# % HISTORY:
# %   17-Oct-2006: Converted from IDL by Jonathan J. Makela
# %   (jmakela@uiuc.edu)

# Define the radius of the Earth in km
    Re = 6371.2

# Convert all input angles from degrees to radians
    el_rad = el*math.pi/180.
    az_rad = az*math.pi/180.

    site_lat_rad = site[0]*math.pi/180
    site_lon_rad = site[1]*math.pi/180

# Calculate the differential angle, alpha
    temp = cos(el_rad)/(1+(ht/Re))
    alpha = acos(temp) - el_rad

# Calculate the pierce point latitude
    temp = sin(site_lat_rad)*cos(alpha) + cos(site_lat_rad)*cos(az_rad)*sin(alpha)
    ipp_lat_rad = asin(temp)

# Calciulate the pierce point longitude
    temp = sin(alpha) * sin(az_rad) / cos(ipp_lat_rad)
    ipp_lon_rad = asin(temp) + site_lon_rad

# Convert radian measurements to degrees
    lat = ipp_lat_rad*180/math.pi
    lon = ipp_lon_rad*180/math.pi
    
    # itemindex = np.where(el<-1)
    # lat[itemindex] = np.nan
    # lon[itemindex] = np.nan
    return lat,lon


def calcbear(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    compass_bearing = 360 - compass_bearing # count degrees clockwise - remove to make counter-clockwise

    return compass_bearing