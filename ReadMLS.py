import pandas as pd
from datetime import time
from datetime import datetime
import numpy as np
import re
import glob
import math
from math import log



#First Code of MLS analysis
# read the MLS data and write it to a csv file

fname = 'aura_mls_l2gpovp_o3_v04_sodankyla.txt'

file = open("/home/poyraden/Analysis/AURA_MLS/mls_data/" + fname, "r")


file.readline()
file.readline()
Ref= file.readline().split(':')[1]
RefPres = [0] * 55
for ir in range(55):
    RefPres[ir] = float(Ref.split()[ir])

Pressurestr = ['']*55; PressurePrestr = ['']*55

for ip in range(55):
    Pressurestr[ip] = 'Pressure_'+str(ip+1)
    PressurePrestr[ip] = 'PressurePrecision_'+str(ip+1)
 
columnString = "Datetime MJD2000 Year DOY sec Lat Lon Dis SZA QFlag Conv" 
columnStr = columnString.split(" ")

#columnStr
columnStr = columnStr + Pressurestr + PressurePrestr

df = pd.read_csv(file, sep = "\s *", engine="python", skiprows=18, header = None, names=columnStr)

for i in range(55):
    df[Pressurestr[i]] = df[Pressurestr[i]] * RefPres[i] * 100000
    df[PressurePrestr[i]] = df[PressurePrestr[i]] * RefPres[i] * 100000

# df.tmp = df.Datetime.str.split("T", n = 1, expand = True)
df['Date'] = df.Datetime.str.split("T", n = 1, expand = True)[0]
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['Date'] = df['Date'].dt.strftime('%Y%m%d')


df['timetmp1'] = pd.to_timedelta(df["sec"], unit='s')
df['timetmp2'] = df['timetmp1'].astype('timedelta64[s]')
df['Time1'] = pd.to_datetime(df['timetmp2'])
df['Time2'] = [x.time() for x in df['Time1']]

# df['Time'] = pd.to_timedelta(df["sec"], unit='s')
# df['Time'] = [time.time() for time in df['Time']]


df['DifLat'] = abs(50.80 - df['Lat'])
df['DifLon'] = abs(4.350 - df['Lon'])

df['Time'] = pd.to_timedelta(df["sec"], unit='s')

fout = 'Sodankyla'
df.to_hdf("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLS_Data" + fout + ".hdf", key='df')
df.to_csv("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLS_Data" + fout + ".csv")


