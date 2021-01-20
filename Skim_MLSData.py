import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
from datetime import time
from datetime import datetime

# Second code of the MLS analysis
#get the mls dates from df and write to matched uccle mls dates, MLSUccle_MatchedDates.txt

#df = pd.read_pickle("/home/poyraden/Analysis/AURA_MLS/AURA_MLS_Data.csv")
df = pd.read_hdf("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLS_Data.hdf")


dfd = df.drop_duplicates(['Date'])
dfd['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
dfd['Date'] = dfd['Date'].dt.strftime('%Y%m%d')
mls_dates = dfd['Date'].tolist()

# get the uccle data dates, first skim it to years 2004-2019 
# filet = open("/home/poyraden/Analysis/AURA_MLS/UccleDates.txt", "r")
filet = open("/home/poyraden/Analysis/Homogenization_Analysis/Files/Uccle/DQA/Uccle_DQA_dates.txt", "r")
# filet = open("/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Uccle/DQA/Uccle_NiluDQA_dates.txt", "r")
#
test_lines = filet.readlines()
sizetxt = len(test_lines)
d1 = ['']*sizetxt
dates = ['']* sizetxt

    
years_mls = [''] * 16
yearsmatch = [] 

#mls years 2004-2019
for y in range(2004,2020):
    years_mls[y-2004] = str(y)

for l in range(sizetxt):
    d1[l] = test_lines[l].split(".")[0]
    # dates[l] = d1[l].split("uc")[1]
    dates[l] = d1[l].split("_")[0]
    # dates[l] = '20'+dates[l]  if ( (dates[l].startswith('0')) | (dates[l].startswith('1'))) else '19'+dates[l]
    for iy in range(0,16):
        # print(dates[l], years_mls[iy])

        if(dates[l].startswith(years_mls[iy])): yearsmatch.append(dates[l])

print('len years match', len(yearsmatch))
#print(yearsmatch)
print('mls dates' , len(mls_dates))

# # match the mls dates with uccle dates
match = []

for j in range(len(mls_dates)):
    for k in range(len(yearsmatch)):
        if(mls_dates[j] == yearsmatch[k]):match.append(yearsmatch[k])
        
print('match', len(match))

match = np.asarray(match)

# now skim the MLS data w.r.t match dates

df['Match'] = df["Date"].isin(match)

match_list = df.index[df['Match'] == True].tolist()

with open('MLSUccle_MatchedDatesDQA.txt', 'w') as f:
# with open('MLSUccle_MatchedDatesNiluDQA.txt', 'w') as f:

    for item in match:
        f.write("%s\n" % item)


# #skim df with matched dates
newdf = df.loc[match_list]

newdf['Date'] = pd.to_datetime(newdf['Date'], format='%Y%m%d')
newdf['Date'] = newdf['Date'].dt.strftime('%Y%m%d')

newdf['Time'] = pd.to_datetime(newdf['Time'] + pd.Timestamp(0))
newdf['Time'] = [time.time() for time in newdf['Time']]


distance_list_night = []
distance_list_noon = []
time_list_night = []
time_list_noon = []

print(len(match))

list_data = []

for im in range (len(match)):
    dftmp = newdf[newdf['Date'] == match[im]]
    df_night = dftmp[(dftmp['Time'] > time(0,0,0)) & (dftmp['Time'] < time(6,0,0)) ]
    df_noon = dftmp[(dftmp['Time'] > time(6,0,0))]
    distance = dftmp.Dis.tolist()
    distance_night = df_night.Dis.tolist()
    distance_noon = df_noon.Dis.tolist()
    
    if(len(distance_noon) == 0): distance_noon = distance
    if(len(distance_night) == 0): distance_night = distance

    if(im < 5): 
        print(im, 'all', distance)
        print(im, 'night', distance_night)
        print(im, 'noon', distance_noon)
    min_night = min(distance_night)
    min_noon = min(distance_noon)

    distance_list_night.append(min_night)
    distance_list_noon.append(min_noon)

    dfskim = newdf[(newdf['Date'] == match[im]) & ((newdf['Dis'] == min_night) | ( newdf['Dis'] ==  min_noon))]
    list_data.append(dfskim)


dffinal = pd.concat(list_data,ignore_index=True)

#this is the MLS data to be used to analyze
# dffinal.to_csv("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLSData_MatchedUccleDQA.csv")
# dffinal.to_hdf('/home/poyraden/Analysis/AURA_MLS/New/AURA_MLSData_MatchedUccleDQA.h5', key='df', mode='w')

# dffinal.to_csv("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLSData_MatchedUccleNiluDQA.csv")
# dffinal.to_hdf('/home/poyraden/Analysis/AURA_MLS/New/AURA_MLSData_MatchedUccleNiluDQA.h5', key='df', mode='w')



