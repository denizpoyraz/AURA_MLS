import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns




### not all the data series have the same dates, raw + DQA and presto ones
df1 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_raw.csv")
df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_bkg-pf.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_bkg-pf-eta.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_bkg-pf-eta-pfground.csv")
# df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_Interpolated_bkg-pf-eta-pfground-tpump.csv")

df1 = df1[df1.PreLevel < 216]
# df1 = df1[df1.PreLevel >= 8]
df2 = df2[df2.PreLevel < 216]
# df2 = df2[df2.PreLevel >= 8]

l1 = df1.drop_duplicates(['Date']).Date.tolist()
l2 = df2.drop_duplicates(['Date']).Date.tolist()

common_dates12 = list(set(l1).intersection(set(l2)))
print(len(common_dates12))

df1 = df1[df1['Date'].isin(common_dates12)]
df2 = df2[df2['Date'].isin(common_dates12)]

print(len(df1.drop_duplicates(['Date'])), len(df2.drop_duplicates(['Date'])) )

df1['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)


print('size bin', len(df1.drop_duplicates(['Date']).Date.tolist()) / 16)

fig, ax = plt.subplots(figsize=(17, 9))
# fig, ax = plt.subplots()

ax.set_yscale('log')
df1['PreLevel'] = np.round(df1['PreLevel'],0)

t = df1.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
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
# ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56]
ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56, 68, 82, 100, 121, 146, 177, 215]

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
hm = sns.heatmap(t, vmin=-3, vmax=3, cmap="vlag", xticklabels=xfreq, yticklabels=1,
                 cbar_kws={'label': 'Bkg - Raw / Raw (%)'})

ax.set_xticklabels(xtick_labels, rotation=0)
# ax.set_yticklabels(ytick_labels, rotation = 0)
# plt.xticks(rotation = 0)

plt.xlabel(" ")
# ax.set_ylim([68,8])
Plotname = '2to1_BkgPF_vs_Raw'

plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/StepHeatMaps/' + Plotname + '.png')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/StepHeatMaps/' + Plotname + '.eps')
plt.show()
