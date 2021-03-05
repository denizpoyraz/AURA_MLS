import pandas as pd
import numpy as np
import math
from math import log
from scipy.interpolate import interp1d

# 3rd code of MLS analysis
# write the Uccle data to a df that matches with MLS

problem = open("DQA_ProblematicFiles.txt", "a")


file = open("/home/poyraden/Analysis/AURA_MLS/Codes/MLSSodankyl_MatchedDatesDQA.txt", "r")

# pathfiles = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/DQA/'
pathfiles = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/Current/'


all_lines = file.readlines()
matcheddates = []

for il in all_lines:
    tmp = il.split("\n")[0]
    # print(tmp)
    begin =""
    if int(tmp) <= 20051124: begin = 'SO' + tmp[2:]
    if int(tmp) > 20051124: begin = 'so' + tmp[2:]
    # print(tmp, begin)

    # if int(il) >= "051124" :print(il[2:])
    # tmp = pathfiles + tmp + '_bkg-pf-eta-pfground-tpump.h5'
    tmp = pathfiles + begin + '_rawcurrent.hdf'


    matcheddates.append(tmp)

print(matcheddates[0:10], len(matcheddates))

# mls data frame to read
dfm = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/AURA_MLSData_MatchedSodankyl_DQA.csv")

# list_data = []
listall_data = []

# file_test = matcheddates[300:800]

for filename in matcheddates:
    # print(filename)
    df = pd.read_hdf(filename)
    # df = pd.read_csv(filename)


    # list_data.append(df)

 # now downsample the uccle data remove descent list
    dfn = df[df.Height > 0]
    maxh = dfn.Height.max()

    if len(dfn) < 10:
        print('height problem', filename)
        continue

    index = dfn[dfn["Height"] == maxh].index[0]
    descent_list = dfn[dfn.index > index].index.tolist()
    dfa = dfn.drop(descent_list)

    ##for the frzoen solutions
    dfa = dfa.drop(dfa[(dfa.O3 <= 2) & (dfa.Pair <= 10)].index)

    # skimming for the mls data
    dfas = dfa[(dfa.Pair >= 3) & (dfa.Pair <= 400)]
    # dfas = dfa[(dfa.Pair >= 10) & (dfa.Pair < 422 )]

    # string to get pressure values of the mls
    st = [''] * 55
    for p in range(55):
        st[p] = 'Pressure_' + str(p + 1)

    # previous
    yref = [383.119, 316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159,
            38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678, 12.1153, 10.0000, 8.25404, 6.81292, 5.62341, 4.64159]
    uybin = []

    for y in range(len(yref) - 1):
        tmp = (log(yref[y]) + log(yref[y + 1])) / 2
        uybin.append(math.exp(tmp))
        # means will be calculated between uybin[i] and uybin[i+1]

    size = len(uybin) - 1
    xmean = [0] * size;
    xmedian = [0] * size

    for xb in range(size):
        tmp = dfas[(dfas.Pair < uybin[xb]) & (dfas.Pair >= uybin[xb + 1])]['O3'].tolist()

        if (len(tmp) < 10):
            continue

        if ((np.mean(tmp) > 0)):
            # print(xb, 'posifitf tmp',tmp)

            xmean[xb] = np.mean(tmp)
            xmedian[xb] = np.median(tmp)

            if (xmean[xb] == 0): print('one here ?')

        if ((np.mean(tmp) < 0)):
            tmp = np.array(tmp)
            ind = np.where(tmp < .0)[0]
            new = np.delete(tmp, ind)

            if (int(len(tmp) / len(ind)) < 3):
                continue
            if (len(new) < 10):
                continue

            xmean[xb] = np.mean(new)
            xmedian[xb] = np.median(new)
            if (xmean[xb] == 0): print('two here ?')

        if ((np.mean(tmp) == 0)):
            xmean[xb] = np.nan

    for aa in range(size):
        if (xmean[aa] == 0):
            # print(dfas.iloc[0]['Header_Date'],uybin[aa], aa, xmean[aa])
            xmean[aa] = np.nan

    xuccle = dfas['O3'].tolist()
    yuccle = dfas['Pair'].tolist()

    xuccle = np.array(xuccle)
    yuccle = np.array(yuccle)
    if ((len(xuccle) < 15) | (len(xuccle) == 0)):
        # print('Problem here ? ', header_date)/
        problem.write(str(df.at[df.first_valid_index(), 'Date']) + '\n')
        continue

    indu = np.where(xuccle < 0)[0]

    xuccle = np.delete(xuccle, indu)
    yuccle = np.delete(yuccle, indu)
    if ((len(xuccle) < 10) | (len(xuccle) == 0)):
        continue

    ymain = [316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119,
             31.6228, 26.1016, 21.5443, 17.7828, 14.678, 12.1153, 10.0000, 8.25404, 6.81292, 5.62341]

    if (max(yuccle) < max(ymain)): continue
    # if(min(yuccle) > min(ymain)):continue

    # 5 different linear interpolations
    fl = interp1d(yuccle, xuccle)
    fn = interp1d(yuccle, xuccle, kind='nearest')
    fp = interp1d(yuccle, xuccle, kind='previous')
    fne = interp1d(yuccle, xuccle, kind='next')

    ## try except part
    xinter_linear = [0] * len(ymain);
    xinter_nearest = [0] * len(ymain)
    xinter_previous = [0] * len(ymain)
    xinter_next = [0] * len(ymain)

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
            # print(header_date, ix,  xinter_linear[ix])

    for ir in range(len(xinter_linear)):
        if (xinter_linear[ir] <= 0): xinter_linear[ir] = np.nan
        if (xinter_nearest[ir] <= 0): xinter_nearest[ir] = np.nan
        if (xinter_previous[ir] <= 0): xinter_previous[ir] = np.nan
        if (xinter_next[ir] <= 0): xinter_next[ir] = np.nan

    header_date = df.at[df.first_valid_index(), 'Date']
    ddate = [df.at[df.first_valid_index(), 'Date']] * len(ymain)
    # im = 23
    im = 28
    ##ib = 8
    ib = 6

    dl = dfm.index[dfm.Date == int(header_date)].tolist()
    # print(dl)
    # mlsdate =
    mlspo3 = list(dfm.loc[dl[0], st[ib:im]])
    tim = dfm.loc[dl[0], 'Time']
    mlstime = [tim] * len(ymain)
    # print(header_date,'and', mlstime)
    dis = dfm.loc[dl[0], 'Dis']
    mlsdis = [dis] * len(ymain)
    if (len(dl) == 2):
        mlspo3_two = list(dfm.loc[dl[1], st[ib:im]])
        tim2 = dfm.loc[dl[1], 'Time']

        mlstime_two = [tim2] * len(ymain)
        dis2 = dfm.loc[dl[1], 'Dis']
        mlsdis_two = [dis2] * len(ymain)

    for il in range(len(mlspo3)):
        if (xmean[il] == 0): print('WHY')
        if (mlspo3[il] < 0):
            mlspo3[il] = np.nan
            xmean[il] = np.nan
            xmedian[il] = np.nan
            xinter_linear[il] = np.nan
            xinter_nearest[il] = np.nan
            xinter_previous[il] = np.nan
            xinter_next[il] = np.nan
        if (len(dl) == 2):
            if ((mlspo3_two[il] < 0)):
                mlspo3_two[il] = np.nan
                xmean[il] = np.nan
                xmedian[il] = np.nan
                xinter_linear[il] = np.nan
                xinter_nearest[il] = np.nan
                xinter_previous[il] = np.nan
                xinter_next[il] = np.nan

    dfl = pd.DataFrame(
        columns=['Date', 'Time', 'Dis', 'PreLevel', 'PO3_MLS', 'PO3_UcMean', 'PO3_UcMedian', 'PO3_UcIntLin',
                 'PO3_UcIntNearest', 'PO3_UcIntPre', 'PO3_UcIntNe'])

    if (len(dl) == 1):
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

    if (len(dl) == 2):
        dfl['Date'] = np.concatenate((ddate, ddate))
        dfl['Time'] = np.concatenate((mlstime, mlstime_two))
        dfl['Dis'] = np.concatenate((mlsdis, mlsdis_two))
        dfl['PreLevel'] = np.concatenate((ymain, ymain))
        dfl['PO3_MLS'] = np.concatenate((mlspo3, mlspo3_two))
        # dfl['PO3_UcMean'] = np.concatenate((xmeanvec,xmeanvec))
        # dfl['PO3_UcMedian'] = np.concatenate((xmedianvec,xmedianvec))
        dfl['PO3_UcMean'] = np.concatenate((xmean, xmean))
        dfl['PO3_UcMedian'] = np.concatenate((xmedian, xmedian))
        dfl['PO3_UcIntLin'] = np.concatenate((xinter_linear, xinter_linear))
        dfl['PO3_UcIntNearest'] = np.concatenate((xinter_nearest, xinter_nearest))
        dfl['PO3_UcIntPre'] = np.concatenate((xinter_previous, xinter_previous))
        dfl['PO3_UcIntNe'] = np.concatenate((xinter_next, xinter_next))

    listall_data.append(dfl)

# Merging all the data files to df

# df = pd.concat(list_data, ignore_index=True)
dfall = pd.concat(listall_data, ignore_index=True)

#
#
# df.to_csv("/home/poyraden/Analysis/AURA_MLS/New/Ucclematched_2004_2019_DQA.csv")
dfall.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_raw.csv")
dfall.to_hdf("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_raw.h5", key = 'df')

# dfall.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_2004-2020_Raw.csv")

# df.to_csv("/home/poyraden/Analysis/AURA_MLS/New/Ucclematched_2004_2019_raw.csv")
# dfall.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_raw.csv")
# print('write dif')
#
# dfcp = dfall.copy()
#
# dfcp['Dif_UcMean'] = np.asarray(dfall.PO3_UcMean) - np.asarray(dfall.PO3_MLS)
# dfcp['Dif_UcMedian'] = np.asarray(dfall.PO3_UcMedian) - np.asarray(dfall.PO3_MLS)
# dfcp['Dif_UcIntLin'] = np.asarray(dfall.PO3_UcIntLin) - np.asarray(dfall.PO3_MLS)
#
# dfcp['RDif_UcMean'] = 100 * (np.asarray(dfall.PO3_UcMean) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)
# dfcp['RDif_UcMedian'] = 100 * (np.asarray(dfall.PO3_UcMedian) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)
# dfcp['RDif_UcIntLin'] = 100 * (np.asarray(dfall.PO3_UcIntLin) - np.asarray(dfall.PO3_MLS)) / np.asarray(dfall.PO3_MLS)
#
# dfcp['Dif_UcMean2'] = np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMean)
# dfcp['Dif_UcMedian2'] = np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMedian)
# dfcp['Dif_UcIntLin2'] = np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcIntLin)
#
# dfcp['RDif_UcMean2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMean)) / np.asarray(dfall.PO3_UcMean)
# dfcp['RDif_UcMedian2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcMedian)) / np.asarray(
#     dfall.PO3_UcMedian)
# dfcp['RDif_UcIntLin2'] = 100 * (np.asarray(dfall.PO3_MLS) - np.asarray(dfall.PO3_UcIntLin)) / np.asarray(
#     dfall.PO3_UcIntLin)
#
# # dfcp.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_NiluDQA.csv")
# dfcp.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_bkg-pf-eta-pfground-tpump.csv")
# dfcp.to_hdf("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_bkg-pf-eta-pfground-tpump.hdf", key = 'df')

# dfcp.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_raw.csv")
# dfcp.to_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_Raw.csv")

