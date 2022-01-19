# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 08:50:18 2022

@author: juliesi
"""

import glob, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import scipy
import scipy.io as scio
import cartopy.crs as ccrs
from PIL import Image
import matplotlib.colors as colors

siteLocs = {'BJN': [74.5038, 19.0012, 0.026],
            'HOP': [76.5089, 25.0144, 0.014],
            'LYR': [78.147, 16.038, 0.522],
            'NYA': [78.923, 11.929, 0.021],
            'HOR': [77.000,15.550,0.010]}
### define path from where to take the GPS files that were saved as .pkl
path="../GPS/"
#### define path where to plot the results
path_res="../publication/"

#### path for allsky imagers
path_allsky="../allsky_LYR/5577/"

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

GPStow_start=datetime(1980,1,6,0,0,0)


##### here this is very long as I saved so many in individual files.
##you can combine these maybe earlier or make a loop to read all of them in
GPS_nya=pd.read_pickle(path+'GPS_NYA_22-02_green.pkl') 
TEC_gps_nya=pd.read_pickle(path+'TEC_NYA_22-02_green_gps.pkl') 

GAL_nya=pd.read_pickle(path+'GAL_NYA_22-02_green.pkl') 
TEC_gal_nya=pd.read_pickle(path+'TEC_NYA_22-02_green_gal.pkl') 

GLO_nya=pd.read_pickle(path+'GLO_NYA_22-02_green.pkl') 
TEC_glo_nya=pd.read_pickle(path+'TEC_NYA_22-02_green_glo.pkl') 




GPS_lyr=pd.read_pickle(path+'GPS_LYR_22-02_green.pkl') 
TEC_gps_lyr=pd.read_pickle(path+'TEC_LYR_22-02_green_gps.pkl') 

GAL_lyr=pd.read_pickle(path+'GAL_LYR_22-02_green.pkl') 
TEC_gal_lyr=pd.read_pickle(path+'TEC_LYR_22-02_green_gal.pkl') 

GLO_lyr=pd.read_pickle(path+'GLO_LYR_22-02_green.pkl') 
TEC_glo_lyr=pd.read_pickle(path+'TEC_LYR_22-02_green_glo.pkl') 



GPS_hor=pd.read_pickle(path+'GPS_HOR_22-02_green.pkl') 
TEC_gps_hor=pd.read_pickle(path+'TEC_HOR_22-02_green_gps.pkl') 

GAL_hor=pd.read_pickle(path+'GAL_HOR_22-02_green.pkl') 
TEC_gal_hor=pd.read_pickle(path+'TEC_HOR_22-02_green_gal.pkl') 

GLO_hor=pd.read_pickle(path+'GLO_HOR_22-02_green.pkl') 
TEC_glo_hor=pd.read_pickle(path+'TEC_HOR_22-02_green_glo.pkl') 




GPS_hop=pd.read_pickle(path+'GPS_HOP_22-02_green.pkl') 
TEC_gps_hop=pd.read_pickle(path+'TEC_HOP_22-02_green_gps.pkl') 

GAL_hop=pd.read_pickle(path+'GAL_HOP_22-02_green.pkl') 
TEC_gal_hop=pd.read_pickle(path+'TEC_HOP_22-02_green_gal.pkl') 

GLO_hop=pd.read_pickle(path+'GLO_HOP_22-02_green.pkl') 
TEC_glo_hop=pd.read_pickle(path+'TEC_HOP_22-02_green_glo.pkl') 



GPS_bjn=pd.read_pickle(path+'GPS_BJN_22-02_green.pkl') 
TEC_gps_bjn=pd.read_pickle(path+'TEC_BJN_22-02_green_gps.pkl') 

GAL_bjn=pd.read_pickle(path+'GAL_BJN_22-02_green.pkl') 
TEC_gal_bjn=pd.read_pickle(path+'TEC_BJN_22-02_green_gal.pkl') 

GLO_bjn=pd.read_pickle(path+'GLO_BJN_22-02_green.pkl') 
TEC_glo_bjn=pd.read_pickle(path+'TEC_BJN_22-02_green_glo.pkl')






### just some checks here how many PRNs I have etc can be removed not used here
PRNvar_gps=GPS_nya.PRN.unique()
PRNvar_glo=GLO_nya.PRN.unique()
PRNvar_gal=GAL_nya.PRN.unique()
Var=GPS_nya.columns[8:16]

Sig_Type_gps=GPS_nya.SigType.unique()
Sig_Type_gal=GAL_nya.SigType.unique()
Sig_Type_glo=GLO_nya.SigType.unique()
Prim_Type_gps=TEC_gps_nya.PrimSig.unique()
Prim_Type_glo=TEC_glo_nya.PrimSig.unique()
Prim_Type_gal=TEC_gal_nya.PrimSig.unique()
Sec_Sig_gal=TEC_gal_nya.SecSig.unique() 
Sec_Sig_gps=TEC_gps_nya.SecSig.unique() 
Sec_Sig_glo=TEC_glo_nya.SecSig.unique() 


#################### here I insert the calibration file and 
                    #choose as all all-sky images the green aurora ones-5577nm

calib = scio.readsav(path_allsky+'lyr5_20200222_5577_cal.dat')  
################################## choose red or green aurora
files_allsky=np.array(glob.glob(path_allsky+'*5577_cal.png', recursive=True))
################################ insert the correct day here

Date_Sel=20200222183108 ### start date
Date_End=20200222235900 ### end date

s_square = [2,10,50,100,170]   ### size of the markes of scintillation indices
sm = plt.cm.ScalarMappable(cmap='tab20', norm=plt.Normalize(vmin=0, vmax=32))
sm.set_array([])
a=np.array([os.path.basename(files_allsky[j]) for j in range(0,len(files_allsky))])
Dates_string=np.array([b[5:13]+b[14:20] for b in a])
Dates_all=np.array([pd.to_datetime(b[5:13]+b[14:20]) for b in a])


### following can probably also be shortened for efficiency, just reducing the dates to be in between min or max
selection=files_allsky[Dates_all>=pd.to_datetime(Date_Sel,format='%Y%m%d%H%M%S')]
Date=Dates_all[Dates_all>=pd.to_datetime(Date_Sel,format='%Y%m%d%H%M%S')]
Dates_str=Dates_string[Dates_all>=pd.to_datetime(Date_Sel,format='%Y%m%d%H%M%S')]

selection=selection[Date<=pd.to_datetime(Date_End,format='%Y%m%d%H%M%S')]
Dates_str=Dates_str[Date<=pd.to_datetime(Date_End,format='%Y%m%d%H%M%S')]
Date=Date[Date<=pd.to_datetime(Date_End,format='%Y%m%d%H%M%S')]

matplotlib.rcParams.update({'font.size': 21})
##################loop through all images in a day
for j in range(0,len(selection),1):
         
            img = Image.open(selection[j])
     
    
     
            data = np.asarray(img)
            data=np.flipud(data)
            data_cal = (data)*calib.conversion_factor/1000 #### divided by 100 -kR
             
            # data_cal = ma.masked_where(data_cal <= 0, data_cal)
             #data_cal = np.log10(data_cal)
             #data_cal[isneginf(data_cal)]=0.
            calib['glons'] = calib['glons'][tuple(scipy.ndimage.distance_transform_edt(np.isnan(calib['glons']), return_distances=False, return_indices=True))]
            calib['glats'] = calib['glats'][tuple(scipy.ndimage.distance_transform_edt(np.isnan(calib['glats']), return_distances=False, return_indices=True))]
                           
                       
            GPSnear=nearest(GPS_nya.TOWDate,Date[j]) ### find nearest scintillation indices to all sky imager dates
            GPShornear=nearest(GPS_hor.TOWDate,Date[j])
            GPSlyrnear=nearest(GPS_lyr.TOWDate,Date[j])
            GPSbjnnear=nearest(GPS_bjn.TOWDate,Date[j])
            GPShopnear=nearest(GPS_hop.TOWDate,Date[j])
            
             ### cut off angle of 15 degrees and drop duplicates in all sets
             
            GPSsubnya=GPS_nya[(GPS_nya.TOWDate==GPSnear)&( GPS_nya.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last') 
            GLOsubnya=GLO_nya[(GLO_nya.TOWDate==GPSnear)&( GLO_nya.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GALsubnya=GAL_nya[(GAL_nya.TOWDate==GPSnear)&( GAL_nya.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            
            
            GPSsubhor=GPS_hor[(GPS_hor.TOWDate==GPShornear)&( GPS_hor.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GLOsubhor=GLO_hor[(GLO_hor.TOWDate==GPShornear)&( GLO_hor.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GALsubhor=GAL_hor[(GAL_hor.TOWDate==GPShornear)&( GAL_hor.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            
            GPSsublyr=GPS_lyr[(GPS_lyr.TOWDate==GPSlyrnear)&( GPS_lyr.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GLOsublyr=GLO_lyr[(GLO_lyr.TOWDate==GPSlyrnear)&( GLO_lyr.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GALsublyr=GAL_lyr[(GAL_lyr.TOWDate==GPSlyrnear)&( GAL_lyr.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            
            
            GPSsubbjn=GPS_bjn[(GPS_bjn.TOWDate==GPSbjnnear)&( GPS_bjn.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GLOsubbjn=GLO_bjn[(GLO_bjn.TOWDate==GPSbjnnear)&( GLO_bjn.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GALsubbjn=GAL_bjn[(GAL_bjn.TOWDate==GPSbjnnear)&( GAL_bjn.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            
            
            GPSsubhop=GPS_hop[(GPS_hop.TOWDate==GPShopnear)&( GPS_hop.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GLOsubhop=GLO_hop[(GLO_hop.TOWDate==GPShopnear)&( GLO_hop.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            GALsubhop=GAL_hop[(GAL_hop.TOWDate==GPShopnear)&( GAL_hop.Elv>=15)].sort_values('60SecSigma').drop_duplicates('PRN', keep='last')
            
            
          
            
            ### reset index after dropping duplicates
            LYRsub = pd.concat([GALsublyr,GPSsublyr,GLOsublyr]).reset_index(drop=True)
            HORsub = pd.concat([GALsubhor,GPSsubhor,GLOsubhor]).reset_index(drop=True)
            NYAsub = pd.concat([GALsubnya,GPSsubnya,GLOsubnya]).reset_index(drop=True)
            HOPsub = pd.concat([GALsubhop,GPSsubhop,GLOsubhop]).reset_index(drop=True)
            BJNsub = pd.concat([GALsubbjn,GPSsubbjn,GLOsubbjn]).reset_index(drop=True)
#### plot figure
            fig = plt.figure(figsize=(15, 10))
            ax = plt.axes(projection=ccrs.AzimuthalEquidistant(central_longitude=15))
            mapi = ccrs.PlateCarree()
         
            
            im=plt.pcolormesh(calib.glons,calib.glats,data_cal, transform=mapi,cmap='cividis',norm=colors.LogNorm(vmin=data_cal.min(), vmax=data_cal.max()))
            
            #### this is just to decide for which magnitude of scintillation which marker to plot
            
            
            for i in NYAsub.index:
                if NYAsub['60SecSigma'][i] < 0.2:
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='o',s=s_square[0],color='r',transform=mapi)    
                   # ax.annotate(NYAsub.PRN[i], (NYAsub.long[i],NYAsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (NYAsub['60SecSigma'][i] >= 0.2) and (NYAsub['60SecSigma'][i] < 0.3):
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='o',s=s_square[1],color='r',transform=mapi)    
                    #ax.annotate(NYAsub.PRN[i], (NYAsub.long[i],NYAsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (NYAsub['60SecSigma'][i] >= 0.3) and (NYAsub['60SecSigma'][i] < 0.5):
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='o',s=s_square[2],color='r',transform=mapi)    
                    ax.annotate(NYAsub.PRN[i], (NYAsub.long[i]+0.1,NYAsub.lat[i]+0.1),color='r',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (NYAsub['60SecSigma'][i] >= 0.5) and (NYAsub['60SecSigma'][i] < 0.7):
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='o',s=s_square[3],color='r',transform=mapi)    
                    ax.annotate(NYAsub.PRN[i], (NYAsub.long[i]+0.1,NYAsub.lat[i]+0.1),color='r',xycoords=mapi._as_mpl_transform(ax),fontsize='20') 
                if (NYAsub['60SecSigma'][i] >= 0.7):
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='o',s=s_square[4],color='r',transform=mapi)    
                    ax.annotate(NYAsub.PRN[i], (NYAsub.long[i]+0.1,NYAsub.lat[i]+0.1),color='r',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                    ax.scatter(NYAsub.long[i],NYAsub.lat[i],marker='+',s=s_square[1],color='k',transform=mapi)  
            for i in LYRsub.index:
                if LYRsub['60SecSigma'][i] < 0.2:
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='o',s=s_square[0],color='lime',transform=mapi)    
                   # ax.annotate(LYRsub.PRN[i], (LYRsub.long[i],LYRsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (LYRsub['60SecSigma'][i] >= 0.2) and (LYRsub['60SecSigma'][i] < 0.3):
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='o',s=s_square[1],color='lime',transform=mapi)    
                    #ax.annotate(LYRsub.PRN[i], (LYRsub.long[i],LYRsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (LYRsub['60SecSigma'][i] >= 0.3) and (LYRsub['60SecSigma'][i] < 0.5):
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='o',s=s_square[2],color='lime',transform=mapi)    
                    ax.annotate(LYRsub.PRN[i], (LYRsub.long[i]+0.1,LYRsub.lat[i]+0.1),color='lime',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (LYRsub['60SecSigma'][i] >= 0.5) and (LYRsub['60SecSigma'][i] < 0.7):
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='o',s=s_square[3],color='lime',transform=mapi)    
                    ax.annotate(LYRsub.PRN[i], (LYRsub.long[i]+0.1,LYRsub.lat[i]+0.1),color='lime',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                if (LYRsub['60SecSigma'][i] >= 0.7):
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='o',s=s_square[4],color='lime',transform=mapi)    
                    ax.annotate(LYRsub.PRN[i], (LYRsub.long[i]+0.1,LYRsub.lat[i]+0.1),color='lime',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                    ax.scatter(LYRsub.long[i],LYRsub.lat[i],marker='+',s=s_square[1],color='lime',transform=mapi)  
            for i in HORsub.index:
                if HORsub['60SecSigma'][i] < 0.2:
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='o',s=s_square[0],color='cyan',transform=mapi)    
                    #ax.annotate(HORsub.PRN[i], (HORsub.long[i],HORsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HORsub['60SecSigma'][i] >= 0.2) and (HORsub['60SecSigma'][i] < 0.3):
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='o',s=s_square[1],color='cyan',transform=mapi)    
                    #ax.annotate(HORsub.PRN[i], (HORsub.long[i],HORsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HORsub['60SecSigma'][i] >= 0.3) and (HORsub['60SecSigma'][i] < 0.5):
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='o',s=s_square[2],color='cyan',transform=mapi)    
                    ax.annotate(HORsub.PRN[i], (HORsub.long[i]+0.1,HORsub.lat[i]+0.1),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HORsub['60SecSigma'][i] >= 0.5) and (HORsub['60SecSigma'][i] < 0.7):
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='o',s=s_square[3],color='cyan',transform=mapi)    
                    ax.annotate(HORsub.PRN[i], (HORsub.long[i]+0.1,HORsub.lat[i]+0.1),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                if (HORsub['60SecSigma'][i] >= 0.7):
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='o',s=s_square[4],color='cyan',transform=mapi)    
                    ax.annotate(HORsub.PRN[i], (HORsub.long[i]+0.1,HORsub.lat[i]+0.1),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                    ax.scatter(HORsub.long[i],HORsub.lat[i],marker='+',s=s_square[1],color='k',transform=mapi)  
                    
  
            for i in HOPsub.index:
                if HOPsub['60SecSigma'][i] < 0.2:
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='o',s=s_square[0],color='magenta',transform=mapi)    
                    #ax.annotate(HOPsub.PRN[i], (HOPsub.long[i],HOPsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HOPsub['60SecSigma'][i] >= 0.2) and (HOPsub['60SecSigma'][i] < 0.3):
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='o',s=s_square[1],color='magenta',transform=mapi)    
                    #ax.annotate(HOPsub.PRN[i], (HOPsub.long[i],HOPsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HOPsub['60SecSigma'][i] >= 0.3) and (HOPsub['60SecSigma'][i] < 0.5):
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='o',s=s_square[2],color='magenta',transform=mapi)    
                    ax.annotate(HOPsub.PRN[i], (HOPsub.long[i]+0.1,HOPsub.lat[i]+0.1),color='magenta',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (HOPsub['60SecSigma'][i] >= 0.5) and (HOPsub['60SecSigma'][i] < 0.7):
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='o',s=s_square[3],color='magenta',transform=mapi)    
                    ax.annotate(HOPsub.PRN[i], (HOPsub.long[i]+0.1,HOPsub.lat[i]+0.1),color='magenta',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                if (HOPsub['60SecSigma'][i] >= 0.7):
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='o',s=s_square[4],color='magenta',transform=mapi)    
                    ax.annotate(HOPsub.PRN[i], (HOPsub.long[i]+0.1,HOPsub.lat[i]+0.1),color='magenta',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                    ax.scatter(HOPsub.long[i],HOPsub.lat[i],marker='+',s=s_square[1],color='k',transform=mapi)                    
                    
            for i in BJNsub.index:
                if BJNsub['60SecSigma'][i] < 0.2:
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='o',s=s_square[0],color='orange',transform=mapi)    
                    #ax.annotate(BJNsub.PRN[i], (BJNsub.long[i],BJNsub.lat[i]),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (BJNsub['60SecSigma'][i] >= 0.2) and (BJNsub['60SecSigma'][i] < 0.3):
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='o',s=s_square[1],color='cyan',edgecolor = 'orange',transform=mapi)    
                    #ax.annotate(BJNsub.PRN[i], (BJNsub.long[i],BJNsub.lat[i]),color='orange',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (BJNsub['60SecSigma'][i] >= 0.3) and (BJNsub['60SecSigma'][i] < 0.5):
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='o',s=s_square[2],color='orange',transform=mapi)    
                    ax.annotate(BJNsub.PRN[i], (BJNsub.long[i]+0.1,BJNsub.lat[i]+0.1),color='orange',xycoords=mapi._as_mpl_transform(ax),fontsize='15')
                if (BJNsub['60SecSigma'][i] >= 0.5) and (BJNsub['60SecSigma'][i] < 0.7):
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='o',s=s_square[3],color='orange',transform=mapi)    
                    ax.annotate(BJNsub.PRN[i], (BJNsub.long[i]+0.1,BJNsub.lat[i]+0.1),color='orange',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                if (BJNsub['60SecSigma'][i] >= 0.7):
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='o',s=s_square[4],color='orange',transform=mapi)    
                    ax.annotate(BJNsub.PRN[i], (BJNsub.long[i]+0.1,BJNsub.lat[i]+0.1),color='orange',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
                    ax.scatter(BJNsub.long[i],BJNsub.lat[i],marker='+',s=s_square[1],color='k',transform=mapi) 
  
  
  
                  
            ax.scatter(siteLocs['HOR'][1],siteLocs['HOR'][0],marker='x',s=s_square[2],color='cyan',transform=mapi)
            ax.annotate('HOR', (siteLocs['HOR'][1]+0.1,siteLocs['HOR'][0]+0.1),color='cyan',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
            ax.scatter(siteLocs['LYR'][1],siteLocs['LYR'][0],marker='x',s=s_square[2],color='lime',transform=mapi)
            ax.annotate('LYR', (siteLocs['LYR'][1]+0.1,siteLocs['LYR'][0]+0.1),color='lime',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
            ax.scatter(siteLocs['NYA'][1],siteLocs['NYA'][0],marker='x',s=s_square[2],color='r',transform=mapi)
            ax.annotate('NYA', (siteLocs['NYA'][1]+0.1,siteLocs['NYA'][0]+0.1),color='r',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
            ax.scatter(siteLocs['BJN'][1],siteLocs['BJN'][0],marker='x',s=s_square[2],color='orange',transform=mapi)
            ax.annotate('BJN', (siteLocs['BJN'][1]+0.1,siteLocs['BJN'][0]+0.1),color='orange',xycoords=mapi._as_mpl_transform(ax),fontsize='20')
            ax.scatter(siteLocs['HOP'][1],siteLocs['HOP'][0],marker='x',s=s_square[2],color='magenta',transform=mapi)
            ax.annotate('HOP', (siteLocs['HOP'][1]+0.1,siteLocs['HOP'][0]+0.1),color='magenta',xycoords=mapi._as_mpl_transform(ax),fontsize='20')

            ax.set_extent([-1, 31, 73.5, 82.5])
          #### more plotting stuff, legend, saving image, color bar etc
            legend_elements = [plt.scatter([], [], marker='o',color='w', s=0, label='σφ [rad]'),
                               plt.scatter([], [], marker='o',color='cyan', s=s_square[0], label='<0.2'),
                               plt.scatter([], [], marker='o', color='cyan', s=s_square[1], label='>0.2'),
                               plt.scatter([], [], marker='o', color='cyan', s=s_square[2], label='>0.3'),
                               plt.scatter([], [], marker='o', color='cyan',s=s_square[3], label='>0.5'),
                               plt.scatter([], [], marker='o', color='cyan',s=s_square[4], label='>0.7')]#,

            ax.legend(handles=legend_elements, loc='lower left')
            
            ax.set_title("".join(["",Dates_str[j][6:8], "/",Dates_str[j][4:6], "/",Dates_str[j][0:4], " ",Dates_str[j][8:10], ":", Dates_str[j][10:12], ":", Dates_str[j][12:14], " UT, ASI: LYR (557.7 nm)"]))
            ax.coastlines(resolution='10m', color = "black", linewidth = 1.5)
            ax.coastlines(resolution='10m', color = "white", linewidth = 1)
            ax.gridlines(draw_labels=False)
            
            vmin = 20
            vmax = 80
            ticks = np.arange(vmin, vmax+.1, 10)
 

            im.set_clim(vmin=vmin, vmax=vmax)
            clb = plt.colorbar(im, ax=ax)
            clb.minorticks_off()
            clb.set_ticks(ticks)
            clb.set_ticklabels([f"{t:.0f}" for t in ticks])
            clb.set_label('[kR]', labelpad=-40, y=1.05, rotation=0)
            os.path
            print(os.getcwd())

            plt.savefig(path_res+Dates_str[j]+'_LYR.png') ###,bbox_inches = 'tight' ) add in the end, if tight layout is wanted
          
         