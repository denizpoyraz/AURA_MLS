import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText
from math import log
from datetime import time
from datetime import datetime
from scipy import signal
from scipy.interpolate import interp1d

# 3rd code of MLS analysis
# write the Uccle data to a df that matches with MLS

problem = open("ProblematicFiles.txt", "a")

#file = open("/home/poyraden/Analysis/AURA_MLS/MatchedDates.txt", "r")
file = open("/home/poyraden/Analysis/AURA_MLS/MatchedDates.txt", "r")


all_lines = file.readlines()
matcheddates = []
for il in all_lines:
    tmp = il.split("\n")[0]
    matcheddates.append(tmp)
print(len(matcheddates))

#fileu = open("/home/poyraden/Analysis/AURA_MLS/UccleData_2004_2018.txt", "r")
fileu = open("/home/poyraden/Analysis/AURA_MLS/UccleData_2004_2018.txt", "r")

test_lines = fileu.readlines()

uccledata_list = ['']*len(test_lines)

for il in range(len(test_lines)):
    test_lines[il] = test_lines[il].split("\n")[0]
    tmp = test_lines[il].split(".")[0].split("uc")[1]
    uccledata_list[il] = str(tmp)

common_dates = set(uccledata_list) & set(matcheddates)
print(len(common_dates))
common_dates = list(common_dates)

file_toread = [] 

for ib in test_lines:
    for d in common_dates:
        if(ib.find(d) != -1): 
            #file_toread.append('/home/poyraden/Analysis/AURA_MLS/UccleData/' + ib)
            file_toread.append('/home/poyraden/Analysis/AURA_MLS/UccleData/' + ib)


columnString = "Time Altitude Pair Tair Humidity TPump PO3 WindDir WindSp AccumO3"
columnStr = columnString.split(" ")

#mls data frame to read
dfm = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/AURA_MLSData_MatchedUccle.csv")
#dfm = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/AURA_MLSData_MatchedUccle.csv")


list_data = []
listall_data = []

file_test = file_toread[300:800]


for filename in file_toread:
#for filename in file_test:

    file = open(filename,'r')
    file.readline()
    header_tmp = file.readline().split()
    header_date = header_tmp[1]
    header_date = datetime.strptime(header_date, '%Y%m%d')
    header_date = header_date.strftime('%Y%m%d')

    header_time = header_tmp[2]
    header_time = datetime.strptime(header_time, '%H:%M')
    header_time = header_time.strftime('%H:%M:%S')

    #print(header_date, header_time)
    file.readline()
    header_flowarate = file.readline().split()[1]
    header_bkg = file.readline().split()[1]
    header_PAvg = file.readline().split()[1]
    header_PCorr = file.readline().split()[1]
    header_TCorr = file.readline().split()[1]
    header_HumCorr = file.readline().split()[1]
    header_TotO3 = file.readline().split()[1]
    header_TotO3Corr = file.readline().split()[1]
    header_PumpCorr = file.readline().split()[1]
    header_O3burst = file.readline().split()[1]
    
    df = pd.read_csv(filename, sep = "\s *", engine="python", skiprows=13, names=columnStr)

    df = df.join(pd.DataFrame(
        [[header_date,  header_time, header_flowarate, header_bkg, header_PAvg,header_PCorr, header_TCorr,
          header_HumCorr, header_TotO3, header_TotO3Corr, header_PumpCorr,header_O3burst ]],
        index=df.index, 
        columns=['Header_Date','Header_Time','Header_FlowRate','Header_Bkg','Header_PAvg','Header_PCorr','Header_TCorr',
                 'Header_HumCorr','Header_TotO3','Header_TotO3Corr','Header_PumpCorr','Header_O3Burst']
    ))

    # df for all uccle data
    list_data.append(df) 

    # now downsample the uccle data 
   # now downsample the uccle data 
    dfn  = df[df.Altitude > 0 ]
    dfn['Descent'] = dfn.Altitude < dfn.Altitude.shift(2)
    descent_list = dfn.index[dfn['Descent'] == True].tolist()
    # ascent df
    dfa = dfn.drop(descent_list)

## for the frzoen solutions
    dfa = dfa.drop(dfa[ (dfa.PO3 <= 2) & (dfa.Pair <= 10) ].index)

    
    # skimming for the mls data
    dfas = dfa[(dfa.Pair >=3) & (dfa.Pair <= 400 )]
    #dfas = dfa[(dfa.Pair >= 10) & (dfa.Pair < 422 )]

    ymls =  [1000.000, 825.404,681.292,562.341,464.159,383.119,316.228,261.016,215.443,177.828,146.780,121.153,100.000,
             82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,17.7828,14.6780,12.1153,10.0000,8.25404,
             6.81292,  5.62341,4.64159,3.83119,3.16228,2.61016,2.15443,1.77828,1.46780,1.21153, 1.00000, 0.681292,
             0.464159,0.316228,0.215443,0.146780,0.100000,0.0464159,0.0215443,0.0100000, 4.64159e-03 ,2.15443e-03,
             1.00000e-03 ,4.64159e-04 ,2.15443e-04 ,1.00000e-04 ,4.64159e-05 ,2.15443e-05 ,1.00000e-05]

    # string to get pressure values of the mls
    st = ['']*55
    for p in range(55):
        st[p] = 'Pressure_' + str(p+1)
        

    # previous
    yref = [383.119 ,316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159,
            38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678, 12.1153,10.0000,8.25404,6.81292,5.62341,4.64159]
    uybin = []

    for y in range(len(yref)-1):
        tmp = (log(yref[y]) + log(yref[y+1]))/2
        uybin.append(math.exp(tmp))
    #print(uybin)
    #means will be calculated between uybin[i] and uybin[i+1]

    size = len(uybin) -1
    xmean = [0]*size; xmedian = [0]*size
    

    for xb in range(size):
        tmp = dfas[(dfas.Pair < uybin[xb]) & ( dfas.Pair >= uybin[xb+1])]['PO3'].tolist()
        
        if(len(tmp) < 10):
            continue
        
        if( (np.mean(tmp) > 0)):
            #print(xb, 'posifitf tmp',tmp)

            xmean[xb] =  np.mean(tmp)
            xmedian[xb] =  np.median(tmp)
            
            if(xmean[xb] == 0): print('one here ?')

        if( (np.mean(tmp) < 0)  ):
            tmp = np.array(tmp)
            ind = np.where(tmp == -9999.0)[0]
            new = np.delete(tmp, ind)

            if (int(len(tmp)/len(ind)) < 3 ):
                continue
            if(len(new) < 10 ):
                continue

            xmean[xb] =  np.mean(new)
            xmedian[xb] =  np.median(new)
            if(xmean[xb] == 0): print('two here ?')

        if( (np.mean(tmp) == 0)  ):
            xmean[xb] = np.nan


    for aa in range(size):
        if(xmean[aa] ==0):
            #print(dfas.iloc[0]['Header_Date'],uybin[aa], aa, xmean[aa])
            xmean[aa] = np.nan
        
    #print('Last',  dfas.iloc[0]['Header_Date'], 'xmean', xmean)  
     
    #Method 2: scipy interpolation
    #xuccle = dfas[(dfas.Pair <= 349)]['PO3'].tolist()
    #yuccle = dfas[(dfas.Pair <=  349)]['Pair'].tolist()
    ## test debug
    xuccle = dfas['PO3'].tolist()
    yuccle = dfas['Pair'].tolist()

    # xuccle = dfas[(dfas.Pair <=  260)]['PO3'].tolist()
    # yuccle = dfas[(dfas.Pair <=  260)]['Pair'].tolist()

    xuccle = np.array(xuccle)
    yuccle = np.array(yuccle)
    if( (len(xuccle) < 15) | (len(xuccle) ==0)):
        print('Problem here ? ', header_date)
        problem.write(header_date + '\n')
        continue
    
    indu = np.where(xuccle < 0)[0]
    
    xuccle = np.delete(xuccle, indu)
    yuccle = np.delete(yuccle, indu)
    if( (len(xuccle) < 10) | (len(xuccle) ==0)):
        continue

    #print('yuccle', yuccle)
    #print('xuccle', xuccle)

    if(header_date == '20150731'):continue
    if(header_date == '20170201'):continue
    if(header_date == '20171006'):continue

    
    #ymain = [316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678]
    #ymain = [215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678]
    ymain = [316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119,
             31.6228, 26.1016, 21.5443, 17.7828, 14.678,12.1153,10.0000,8.25404,6.81292,5.62341]

    if(max(yuccle) < max(ymain)):continue
    # if(min(yuccle) > min(ymain)):continue

    #ymain = np.array(ymain)

    #indym = np.where(min(yuccle) > ymain)[0]
    #ymain[indym] = 0
    # if(len(xmeanvec) != len(ymain)): print(header_date)

    #print(len(xuccle), len(yuccle))
    # 5 different linear interpolations
    fl = interp1d(yuccle, xuccle)
    #fc = interp1d(yuccle, xuccle, kind='cubic')
    fn = interp1d(yuccle, xuccle, kind='nearest')
    fp = interp1d(yuccle, xuccle, kind='previous')
    fne = interp1d(yuccle, xuccle, kind='next')

   
    # xinter_linear = fl(ymain)
    # #xinter_cubic = fc(ymain)
    # xinter_nearest = fn(ymain)
    # xinter_previous = fp(ymain)
    # xinter_next = fne(ymain)

     ## try except part
    xinter_linear = [0]* len(ymain); xinter_nearest =  [0]* len(ymain)
    xinter_previous =  [0]* len(ymain)
    xinter_next =  [0]* len(ymain)

    for ix in range(len(ymain)):
        try:
            xinter_linear[ix] = fl(ymain[ix])
            xinter_nearest[ix] = fn(ymain[ix])
            xinter_previous[ix] = fp(ymain[ix])
            xinter_next[ix] = fne(ymain[ix])
        except ValueError:
            xinter_linear[ix] = np.nan
            xinter_nearest[ix] = np.nan
            xinter_previous[ix] = np.nan
            xinter_next[ix] = np.nan
            #print(header_date, ix,  xinter_linear[ix])


    for ir in range(len(xinter_linear)):
        if(xinter_linear[ir] <= 0): xinter_linear[ir] = np.nan
        if(xinter_nearest[ir] <= 0): xinter_nearest[ir] = np.nan
        if(xinter_previous[ir] <= 0): xinter_previous[ir] = np.nan
        if(xinter_next[ir] <= 0): xinter_next[ir] = np.nan
    
    ddate = [header_date] * len(ymain)
    #im = 23
    im = 28
    ##ib = 8
    ib = 6
    
    dl = dfm.index[dfm.Date == int(header_date)].tolist()
    #mlsdate = 
    mlspo3 = list(dfm.loc[dl[0],st[ib:im]])
    tim = dfm.loc[dl[0],'Time']
    mlstime = [tim] * len(ymain)
    #print(header_date,'and', mlstime)
    dis =  dfm.loc[dl[0],'Dis']
    mlsdis = [dis]*len(ymain)
    if(len(dl) == 2 ):
        mlspo3_two = list(dfm.loc[dl[1],st[ib:im]])
        tim2 = dfm.loc[dl[1],'Time']
        mlstime_two =  [tim2]* len(ymain)
        dis2 = dfm.loc[dl[1],'Dis'] 
        mlsdis_two = [dis2] * len(ymain)
        
    for il in range(len(mlspo3)):
        if(xmean[il] == 0 ): print('WHY')
        if(mlspo3[il] < 0):
            mlspo3[il]= np.nan
            xmean[il] = np.nan
            xmedian[il] = np.nan
            xinter_linear[il] = np.nan
            xinter_nearest[il] = np.nan
            xinter_previous[il] = np.nan
            xinter_next[il] = np.nan
        if(len(dl) == 2):
            if((mlspo3_two[il] < 0)):
                mlspo3_two[il]=  np.nan
                xmean[il] = np.nan
                xmedian[il] = np.nan
                xinter_linear[il] = np.nan
                xinter_nearest[il] = np.nan
                xinter_previous[il] = np.nan
                xinter_next[il] = np.nan

    dfl = pd.DataFrame(columns=['Date', 'Time', 'Dis', 'PreLevel','PO3_MLS', 'PO3_UcMean', 'PO3_UcMedian', 'PO3_UcIntLin', 'PO3_UcIntNearest', 'PO3_UcIntPre','PO3_UcIntNe'])

    
    if(len(dl) == 1 ):
        dfl['Date'] = ddate
        dfl['Time'] = np.asarray(mlstime)
        dfl['Dis'] = np.asarray(mlsdis)
        dfl['PreLevel'] = np.asarray(ymain)
        dfl['PO3_MLS'] = mlspo3
        dfl['PO3_UcMean'] = xmean
        dfl['PO3_UcMedian'] = xmedian
        dfl['PO3_UcIntLin'] = xinter_linear
        dfl['PO3_UcIntNearest'] = xinter_nearest
        dfl['PO3_UcIntPre'] = xinter_previous
        dfl['PO3_UcIntNe'] = xinter_next
        
    if(len(dl) == 2 ):
        dfl['Date'] = np.concatenate((ddate,ddate))
        dfl['Time'] = np.concatenate((mlstime, mlstime_two))
        dfl['Dis'] = np.concatenate((mlsdis, mlsdis_two))
        dfl['PreLevel'] = np.concatenate((ymain,ymain))
        dfl['PO3_MLS'] = np.concatenate((mlspo3,mlspo3_two))
        #dfl['PO3_UcMean'] = np.concatenate((xmeanvec,xmeanvec))
        #dfl['PO3_UcMedian'] = np.concatenate((xmedianvec,xmedianvec))
        dfl['PO3_UcMean'] = np.concatenate((xmean,xmean))
        dfl['PO3_UcMedian'] = np.concatenate((xmedian,xmedian))
        dfl['PO3_UcIntLin'] = np.concatenate((xinter_linear,xinter_linear))
        dfl['PO3_UcIntNearest'] = np.concatenate((xinter_nearest,xinter_nearest))
        dfl['PO3_UcIntPre'] = np.concatenate((xinter_previous,xinter_previous))
        dfl['PO3_UcIntNe'] = np.concatenate((xinter_next, xinter_next))


        
    listall_data.append(dfl) 

# Merging all the data files to df

df = pd.concat(list_data,ignore_index=True)
dfall = pd.concat(listall_data,ignore_index=True)



df.to_csv("/home/poyraden/Analysis/AURA_MLS/Ucclematched_2004_2018_db_DC.csv")
dfall.to_csv("/home/poyraden/Analysis/AURA_MLS/MLS_UccleInterpolated_2004-2018_final_DC.csv")

print('write dif')

dfcp = dfall.copy() 

dfcp['Dif_UcMean'] = np.asarray(dfall.PO3_UcMean) - np.asarray(dfall.PO3_MLS) 
dfcp['Dif_UcMedian'] = np.asarray(dfall.PO3_UcMedian) - np.asarray(dfall.PO3_MLS) 
dfcp['Dif_UcIntLin'] = np.asarray(dfall.PO3_UcIntLin) - np.asarray(dfall.PO3_MLS)


dfcp['RDif_UcMean'] = 100 * (np.asarray(dfall.PO3_UcMean) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)
dfcp['RDif_UcMedian'] = 100 * (np.asarray(dfall.PO3_UcMedian) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)
dfcp['RDif_UcIntLin'] = 100 * (np.asarray(dfall.PO3_UcIntLin) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)

dfcp['Dif_UcMean2'] =  np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMean) 
dfcp['Dif_UcMedian2'] = np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMedian) 
dfcp['Dif_UcIntLin2'] =  np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcIntLin) 

dfcp['RDif_UcMean2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMean)) / np.asarray(dfall.PO3_UcMean)
dfcp['RDif_UcMedian2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMedian)) / np.asarray(dfall.PO3_UcMedian)
dfcp['RDif_UcIntLin2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcIntLin)) / np.asarray(dfall.PO3_UcIntLin)

dfcp.to_csv("/home/poyraden/Analysis/AURA_MLS/MLS_UccleInterpolated_2004-2018_Dif_final_DC.csv")

