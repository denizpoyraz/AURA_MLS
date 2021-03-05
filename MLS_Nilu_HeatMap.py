import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### not all the data series have the same dates, raw + DQA and presto ones
df1 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_Raw.csv")
df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_bkg-pf-eta-pfground.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_onlybkg_v2.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_onlyeta.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_onlytpump.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA_onlyPhi.csv")

df1 = df1[df1.PreLevel < 57]
df1 = df1[df1.PreLevel >= 8]
df2 = df2[df2.PreLevel < 57]
df2 = df2[df2.PreLevel >= 8]

l1 = df1.drop_duplicates(['Date']).Date.tolist()
l2 = df2.drop_duplicates(['Date']).Date.tolist()

common_dates12 = list(set(l1).intersection(set(l2)))
print(len(common_dates12))

df1 = df1[df1['Date'].isin(common_dates12)]
df2 = df2[df2['Date'].isin(common_dates12)]

print(len(df1.drop_duplicates(['Date'])), len(df2.drop_duplicates(['Date'])) )

df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df2.PO3_MLS)) / np.asarray(df2.PO3_UcIntLin)


t1 = df1.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t2 = df2.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')

dif_t1t2 = list(set(t1.columns).difference(set(t2.columns)))

dif_t1t2 =[20110209, 20110216, 20110601, 20060427, 20110223, 20100623, 20100630, 20110105, 20100506, 20101020, 20101027,
           20060324, 20051109, 20100901, 20100908, 20100915, 20051124, 20100825, 20110427, 20110302, 20110305, 20110306,
           20100708, 20060517, 20110313, 20110314, 20101229, 20110318, 20101103, 20110326, 20101110, 20100602, 20110206]


for i in dif_t1t2:
    df1 = df1[df1.Date != i]
    df2 = df2[df2.Date != i]

# print(dif_t1t2)


dfr = df2

dfr['RDif_UcIntLin'] = 100 * (np.asarray(dfr.PO3_UcIntLin) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcIntLin)
dfr['PreLeveltmp'] = dfr['PreLevel']

# to make the dataset weekly
# dfr = dfr.set_index('Datenf').groupby('PreLeveltmp').resample('W').mean()
# dfr = dfr.set_index('Datenf').groupby('PreLeveltmp').resample('6M').mean()
# dfr = dfr.drop(['PreLeveltmp'], axis =1)
# dfr = dfr.reset_index(level=[0,1])

print('size bin', len(dfr.drop_duplicates(['Date']).Date.tolist()) / 16)

fig, ax = plt.subplots(figsize=(17, 9))
# fig, ax = plt.subplots()

ax.set_yscale('log')

t = dfr.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
print(len(t.index), len(t.columns))

# original
# xfreq = 283
# xfreq = 123
# xfreq = 123
xfreq = 45  # nilu
# xfreq = 46  # nilu
xfreq = 43

# for all range xtick labels

# weekly
ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56]
# ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56, 68, 82, 100, 121, 146, 177, 215]

# xtick_labels = ['2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2019']
# xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009','2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017' ,'2018','2019']
xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', '2018', '2019', '2020']

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
ax.set_yticklabels(ytick_labels, rotation = 0)
# plt.xticks(rotation = 0)

plt.xlabel(" ")
# ax.set_ylim([68,8])
Plotname = 'Sodankayl_BkgandPFandEtaandPFGround_eccminusmls'

plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.png')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.eps')
plt.show()
