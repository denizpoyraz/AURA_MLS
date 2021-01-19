import pandas as pd
import numpy as np
import math
from math import log
from datetime import datetime
from scipy.interpolate import interp1d
import glob


allFiles = glob.glob("/home/poyraden/Analysis/AURA_MLS/UccleData/uc*")

list_data = []

columnString = "Time Altitude Pair Tair Humidity TPump PO3 WindDir WindSp AccumO3"
columnStr = columnString.split(" ")

for filename in allFiles:
    # for filename in file_test:
    file = open(filename, 'r')
    file.readline()
    header_tmp = file.readline().split()
    header_date = header_tmp[1]
    header_date = datetime.strptime(header_date, '%Y%m%d')
    header_date = header_date.strftime('%Y%m%d')

    header_time = header_tmp[2]
    header_time = datetime.strptime(header_time, '%H:%M')
    header_time = header_time.strftime('%H:%M:%S')

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

    df = pd.read_csv(filename, sep="\s *", engine="python", skiprows=13, names=columnStr)

    df = df.join(pd.DataFrame(
        [[header_date, header_time, header_flowarate, header_bkg, header_PAvg, header_PCorr, header_TCorr,
          header_HumCorr, header_TotO3, header_TotO3Corr, header_PumpCorr, header_O3burst]],
        index=df.index,
        columns=['Header_Date', 'Header_Time', 'Header_FlowRate', 'Header_Bkg', 'Header_PAvg', 'Header_PCorr',
                 'Header_TCorr',
                 'Header_HumCorr', 'Header_TotO3', 'Header_TotO3Corr', 'Header_PumpCorr', 'Header_O3Burst']
    ))


    df.to_csv("/home/poyraden/Analysis/AURA_MLS/UccleData/" + header_date + ".csv")

    list_data.append(df)

dfl = pd.concat(list_data,ignore_index=True)
dfl.to_csv("/home/poyraden/Analysis/AURA_MLS/UccleData/AllCsv/Uccle_PrestoData.csv")



