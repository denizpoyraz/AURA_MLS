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


dfr = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_raw.csv")
# dfr = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/New/MLS_UccleInterpolated_2004-2019_DQA.csv")

# dfr = dfr[dfr.PreLevel < 60]
# 20070611, 20080912, 20150731, 20171006
dfr = dfr[dfr.Date != 20070611 ]
dfr = dfr[dfr.Date != 20080912 ]
dfr = dfr[dfr.Date != 20150731 ]
dfr = dfr[dfr.Date != 20171006 ]


# dfr['Date'] = pd.to_datetime(dfr['Date'], format='%Y%m%d')

# print(dfr['Date'])
# print(list(dfr))

# x_axis_labels = [2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020]

dfr['PreLevel'] = np.round(dfr['PreLevel'],0)

fig, ax = plt.subplots(figsize=(11, 9))
ax.set_yscale('log')

t = dfr.pivot_table(index='PreLevel', columns='Date', values='RDif_UcMean')

# sns.color_palette("vlag", as_cmap=True)
# sns.heatmap(t,  vmin=-5, vmax=5,  cmap="vlag", xticklabels=x_axis_labels)
sns.heatmap(t,  vmin=-50, vmax=50, cmap="vlag")

# ax.set_xticklabels(x_axis_labels)

plt.show()
