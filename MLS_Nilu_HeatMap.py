import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### not all the data series have the same dates, raw + DQA and presto ones
df1 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_Raw.csv")
df2 = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_Sodankayl_RDif_Interpolated_2004-2019_DQA.csv")



dfr = df2


# dfr['RDif_UcMean'] = 100 * (np.asarray(dfr.PO3_UcMean) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcMean)
# dfr['RDif_UcMedian'] = 100 * (np.asarray(dfr.PO3_UcMedian) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcMedian)
dfr['RDif_UcIntLin'] = 100 * (np.asarray(dfr.PO3_UcIntLin) - np.asarray(dfr.PO3_MLS)) / np.asarray(dfr.PO3_UcIntLin)

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
# dfr = dfr[dfr.Pressure < 57]
dfr = dfr[dfr.Pressure >= 8]

t = dfr.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
print(len(t.index), len(t.columns))


# original
# xfreq = 283
# xfreq = 123
# xfreq = 123
# xfreq = 45  # nilu
xfreq = 46  # nilu

# for all range xtick labels

# weekly
ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56]
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
hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag", xticklabels=xfreq, yticklabels=1,
                 cbar_kws={'label': 'ECC - MLS / ECC (%)'})

ax.set_xticklabels(xtick_labels, rotation=0)
ax.set_yticklabels(ytick_labels, rotation = 0)

plt.xlabel(" ")
# ax.set_ylim([68,8])
Plotname = 'Sodankayl_DQA_eccminusmls_niludates_AllRange'

plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.png')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Homogenization/UpDated/' + Plotname + '.eps')
plt.show()
