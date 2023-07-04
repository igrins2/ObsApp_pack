# -*- coding: utf-8 -*-

"""
Created on June 23, 2023

Modified on June 23, 2023

refered from FITSHD_V2 of original IGRINS
@author: hilee
"""

##############################################################
#    IGRINS-2 ObsApp - FITS Header Module                    #
#    Ueejeong Jeong (Kyungpook National University / KASI)   #
##############################################################

FHDARR = [

['INSTRUME' ,'S',  'IGRINS-2'             ,'Name of the instrument'],
['TIMESYS'  ,'S',  'UTC'                  ,'Time system used in this header'],

['EXPTIME'  ,'F2', '$EXPTIME'  ,'Integration time in seconds'],
['TEMP-DET' ,'F1', '$DET_TEMP' ,'Temperature of Detector (K)'],
['TEMP-GRA' ,'F1', '$DET_GRAT' ,'Temperature of Immersion Grating (K)'],
['BAND'     ,'S',  'S'     ,'Band of Spectrum'],
['UTDATE'   ,'S',  '$UTDATE'   ,'UT date as integer in yyyymmdd format'],
['DATE-OBS' ,'S',  '$DATEOBS'  ,'Date time (UTC) of start of observation'],
['DATE-END' ,'S',  '$DATEEND'  ,'Date time (UTC) of end of observation'],
['UT-OBS'   ,'F5', '$UTOBS'    ,'[h], Start time of integration'],
['UT-END'   ,'F5', '$UTEND'    ,'[h], End time of integration'],
['JD-OBS'   ,'F6', '$JDOBS'    ,'DATE-OBS as Julian Date'],
['JD-END'   ,'F6', '$JDEND'    ,'DATE-END as Julian Date'],
['MJD-OBS'  ,'F6', '$MJDOBS'   ,'MJD-OBS as Modified Julian Date'],
['TELPA'    ,'I',  '{tel_para_angle}'    ,'Paralactic Angle'],

['RADECSYS' ,'S','FK5'       ,'Coordinate System'],

['TELRA'    ,'S',  '{tel_ra}'   ,'Current telescope right ascension'],
['TELDEC'   ,'S',  '{tel_dec}'   ,'Current telescope declination'],
['TELEPOCH' ,'F5', '{display_epoch}'  ,'Current telescope epoch'],
['OBJRA'    ,'F8',  '{obj_ra_deg}'   ,'Current object right ascension'],
['OBJDEC'   ,'F8',  '{obj_dec_deg}'   ,'Current object declination'],
['OBJEPOCH' ,'F5', '{obj_epoch}'  ,'Current object epoch'],
['USERRA'   ,'S',  '$USERRA'   ,'User-specified RA'],
['USERDEC'  ,'S',  '$USERDEC'  ,'User-specified Dec.'],
['USEREPOC' ,'F5', '$USEREPOC'  ,'User coord epoch'],
['FOCUSVAL' ,'I',  '{focus}'   ,'Telescope focus value'],
['AUTOGUID' ,'S',  '-'   ,'Autoguiding on/off log'],

['AMSTART'  ,'F3', '{start[tel_airmass]}' ,'Airmass at start of observation'],
['AMEND'    ,'F3', '{end[tel_airmass]}' ,'Airmass at end of observation'],
['HASTART'  ,'S', '{start[tel_hourangle]}' ,'[h] HA at start of run'],
['HAEND'    ,'S', '{end[tel_hourangle]}' ,'[h] HA at end of run'],
['LSTSTART' ,'S', '{start[lst]}' ,'[h] LST at start of run'],
['LSTEND'   ,'S', '{end[lst]}' ,'[h] LST at end of run'],
['ZDSTART'  ,'F5', '{start[tel_zd]}' ,'[d] ZD at start of run'],
['ZDEND'    ,'F5', '{end[tel_zd]}' ,'[d] ZD at end of run'],
['PASTART'  ,'F5', '{start[tel_position_angle]}' ,'[d] rotator position angle at start'],
['PAEND'    ,'F5', '{end[tel_position_angle]}' ,'[d] rotator position angle at end'],

['BARPRESS' ,'F1', '{weather_bar_pressure}'  ,'[mbar][hPa], Ambient pressure'],
['AIRTEMP'  ,'F1', '{weather_temp}'  ,'[degC], Air temperature'],
['HUMIDITY' ,'F1', '{weather_humd}'  ,'[per cent], Relative Humidity'],
['DEWPOINT' ,'F1', '{weather_dewpoint}' ,'[degC], Dewpoint'],

['GAIN'     ,'F2', '2.00' ,'[electrons/ADU], Conversion Gain'],
['NSAMP'    ,'I' , '$DET_NSMP' ,'Number of Fowler Sampling'],
['RDNOISE'  ,'F2', '9.00' ,'Read Noise of Fowler Sampled Image with NSAMP'],

['SLIT_CX'  ,'I', '1024'      ,'Center position of slit in the SVC image'],
['SLIT_CY'  ,'I', '1021'      ,'Center position of slit in the SVC image'],
['SLIT_WID' ,'I', '8'         ,'(px) Width of slit'],
['SLIT_LEN' ,'I', '112'       ,'(px) Length of slit'],
['SLIT_ANG' ,'I', '135'       ,'(d) Position angle of slit in the image']

#DO NOT remove/modify
]
#DO NOT remove/modify

from numpy import isnan, nan

def ValHDLF(fmt, Val, obj, tcs_info, idet=0):
    '''
    FITS header organizer
    '''
    if Val[0] == '$':
        res = getattr(obj, 'FHD_'+Val[1:])
        if isinstance(res, list):
            res = res[idet]
    else:
        res = Val.format(**tcs_info)

    if fmt[0] == 'F':
        return float(('%.'+fmt[1:]+'f')%float(res))
    elif fmt[0] == 'I':
        if res == "nan": # if value was NaN
            return nan
        return int(float(res))
    else:
        return res



