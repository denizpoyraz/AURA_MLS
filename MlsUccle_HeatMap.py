import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker
from math import log
from datetime import time
from datetime import datetime
from scipy import signal
import seaborn as sns

### not all the data series have the same dates, raw + DQA and presto ones
df1 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_raw.csv")
df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_DQA.csv")
df3 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_NiluDQA.csv")
# df3 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_presto.csv")

df1 = df1[df1.Date < 20190101]
df2 = df2[df2.Date < 20190101]
df3 = df3[df3.Date < 20190101]

df1 = df1[df1.Date != 20070611]
df1 = df1[df1.Date != 20080912]
df1 = df1[df1.Date != 20150731]
df1 = df1[df1.Date != 20171006]

df2 = df2[df2.Date != 20070611]
df2 = df2[df2.Date != 20080912]
df2 = df2[df2.Date != 20150731]
df2 = df2[df2.Date != 20171006]

df3 = df3[df3.Date != 20070611 ]
df3 = df3[df3.Date != 20080912 ]
df3 = df3[df3.Date != 20150731 ]
df3 = df3[df3.Date != 20171006 ]

df1 = df1[df1.PreLevel < 57]
df1 = df1[df1.PreLevel >= 8]
df2 = df2[df2.PreLevel < 57]
df2 = df2[df2.PreLevel >= 8]
df3 = df3[df3.PreLevel < 57]
df3 = df3[df3.PreLevel >= 8]

l1 = df1[df1.Date < 20190101].drop_duplicates(['Date']).Date.tolist()
l2 = df2[df2.Date < 20190101].drop_duplicates(['Date']).Date.tolist()
l3 = df3[df3.Date < 20190101].drop_duplicates(['Date']).Date.tolist()

common_dates12 = list(set(l1).intersection(set(l2)))
common_dates13 = list(set(l1).intersection(set(l3)))
common_dates23 = list(set(l2).intersection(set(l3)))

print('check before', len(df1), len(df2), len(df3))

df1 = df1[df1['Date'].isin(common_dates12)]
df1 = df1[df1['Date'].isin(common_dates13)]
df2 = df2[df2['Date'].isin(common_dates12)]
df2 = df2[df2['Date'].isin(common_dates23)]
df3 = df3[df3['Date'].isin(common_dates13)]
df3 = df3[df3['Date'].isin(common_dates23)]


dfr = df1

print(list(df2))
print(list(df3))

print('check', len(df1.drop_duplicates(['Date']).Date.tolist()), len(df2.drop_duplicates(['Date']).Date.tolist()), len(df3.drop_duplicates(['Date']).Date.tolist()))
print('check', len(dfr.drop_duplicates(['Date']).Date.tolist()))

# dfr['RDif_UcMean'] = 100 * (np.asarray(dfr.PO3_UcMean) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcMean)
# dfr['RDif_UcMedian'] = 100 * (np.asarray(dfr.PO3_UcMedian) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcMedian)
dfr['RDif_UcIntLin'] = 100 * (np.asarray(dfr.PO3_UcIntLin) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcIntLin)
df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df2.PO3_MLS)) / np.asarray(df2.PO3_UcIntLin)
df3['RDif_UcIntLin'] = 100 * (np.asarray(df3.PO3_UcIntLin) - np.asarray(df3.PO3_MLS)) / np.asarray(df3.PO3_UcIntLin)

# dfr = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_DQA.csv")
# dfr['Datetmp'] = pd.to_datetime(dfr['Date'], format='%Y%m%d')
# dfr['Datenf'] = pd.to_datetime(dfr['Date'], format='%Y%m%d')
dfr['PreLeveltmp'] = dfr['PreLevel']

# to make the dataset weekly
# dfr = dfr.set_index('Datenf').groupby('PreLeveltmp').resample('W').mean()
# dfr = dfr.set_index('Datenf').groupby('PreLeveltmp').resample('6M').mean()
# dfr = dfr.drop(['PreLeveltmp'], axis =1)
# dfr = dfr.reset_index(level=[0,1])



# print('size bin', len(dfr.drop_duplicates(['Date']).Date.tolist()) / 16)

fig, ax = plt.subplots(figsize=(17, 9))
# fig, ax = plt.subplots()

ax.set_yscale('log')

dfr['Pressure'] = dfr['PreLeveltmp'].astype('int')
dfr = dfr[dfr.Pressure < 57]
dfr = dfr[dfr.Pressure >= 8]

t1 = df1.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t2 = df2.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t3 = df3.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')

dif_t2t3 = list(set(t2.columns).difference(set(t3.columns)))

for i in dif_t2t3:
    print(i)
    dfr = dfr[dfr.Date != i]
    df2 = df2[df2.Date != i]
    df3 = df3[df3.Date != i]

print(dif_t2t3)

t = dfr.pivot_table(index='Pressure', columns='Date', values='RDif_UcIntLin')
t1 = df1.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t2 = df2.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t3 = df3.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')


print(len(t.index), len(t.columns))
print(len(t1.index), len(t2.columns))
print(len(t2.index), len(t2.columns))
print(len(t3.index), len(t3.columns))

# original
# xfreq = 283
# xfreq = 123
# xfreq = 123
xfreq = 92  # nilu
# for all range xtick labels

# weekly
ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56]
# xtick_labels = ['2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2019']
# xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009','2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017' ,'2018','2019']
xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', '2018']

##monthly
# xticks_labels = [' 2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018']
# xfreq = 47
# xfreq = 48
# xfreq = 11
# xfreq = 2

# sns.color_palette("vlag", as_cmap=True)
hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag", xticklabels=xfreq, yticklabels=1,
                 cbar_kws={'label': 'ECC - MLS / ECC (%)'})

ax.set_xticklabels(xtick_labels, rotation=0)
# ax.set_yticklabels(ytick_labels, rotation = 0)

plt.xlabel(" ")
# ax.set_ylim([68,8])
Plotname = 'OriginalRaw_eccminusmls_niludates'

plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.png')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.eps')
plt.show()
