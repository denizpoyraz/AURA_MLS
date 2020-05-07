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

def plotyearly(xarray,std_xarray, main_xarray, std_main_xarray, Yax, xranges,  plotlabel, xtitle ,ytitle,plotname):
#def plotyearly(mean_ucint, std_ucint, Y, date_label, 'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_UcIntLinPerYear'):
    
    fig,ax0 = plt.subplots()
    # plt.ylim(250,3)
    plt.xlim(xranges)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    ax0.tick_params(axis='both', which='both', direction='in')
    ax0.yaxis.set_ticks_position('both')
    ax0.xaxis.set_ticks_position('both')
    ax0.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.set_yscale('log')



    colorw = 'blue' #winter
    colorsp = 'green' #spring
    colorsu = 'gold' #summer
    colora  = 'orange'

    ax0.errorbar(xarray[0], Yax, xerr = std_xarray[0], color =colorw,  label = plotlabel[0],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    ax0.errorbar(xarray[1], Yax, xerr = std_xarray[1],color= colorsp,  label = plotlabel[1],  marker = "v",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    ax0.errorbar(xarray[2], Yax, xerr = std_xarray[2], color = colorsu, label = plotlabel[2],  marker = "^",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    ax0.errorbar(xarray[3], Yax, xerr = std_xarray[3], color = colora, label = plotlabel[3],  marker = "<",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)



    ax0.set_yticks([200,160, 120, 100, 80, 70, 60, 50, 40, 30,20, 10,5])


    plt.ylim(250, 4)

    ax0.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax0.errorbar(main_xarray, Yax, xerr = std_main_xarray, label = 'All',  marker = "x", color = 'black', linewidth = 2, elinewidth = 0.5, capsize = 4, capthick=1.0)

    std_p5 = [i + 5 for i in main_xarray]
    std_m5 = [i - 5 for i in main_xarray]

    ax0.axvline(x=0, color='grey', linestyle='--')
    # ax0.axvspan(-5, 5, alpha=0.2, color='grey')
    ax0.fill_betweenx(Yax, std_m5, std_p5, alpha=0.2, facecolor='k')

    ax0.legend(loc='upper right', frameon=True)
    ##, fontsize = 'small')
    #
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Season_0605/PerSeason_' + plotname +'v2.pdf')
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Season_0605/PerSeason_' + plotname +'v2.eps')
    #

    #plt.show()

def plotmeanyearlyOpOne(Xax, Yax, Yxerr, PreLabel, Plotname,inds,ylimit ):
#plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucint2, Ystr, 'Dif_UcMean_215-100',[0,1,2,3,4])

    figY = plt.figure()

    axY5 = figY.add_axes([0.1, 0.7, 0.8, 0.15])
    axY4 = figY.add_axes([0.1, 0.55, 0.8, 0.15])
    axY3 = figY.add_axes([0.1, 0.4, 0.8, 0.15])
    axY2 = figY.add_axes([0.1, 0.25, 0.8, 0.15])
    axY1 = figY.add_axes([0.1, 0.1, 0.8, 0.15])

    axY1.set_ylim(ylimit)
    axY2.set_ylim(ylimit)
    axY3.set_ylim(ylimit)
    axY4.set_ylim(ylimit)
    axY5.set_ylim(ylimit)

    axY1.axhline(y=0, color='grey', linestyle='--')
    axY2.axhline(y=0, color='grey', linestyle='--')
    axY3.axhline(y=0, color='grey', linestyle='--')
    axY4.axhline(y=0, color='grey', linestyle='--')
    axY5.axhline(y=0, color='grey', linestyle='--')

    
    axY5.errorbar( Xax, Yax[inds[4]], yerr = Yxerr[inds[4]],  label = Ystr[inds[4]], marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    axY4.errorbar( Xax, Yax[inds[3]], yerr = Yxerr[inds[3]],  label = Ystr[inds[3]], marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    axY3.errorbar( Xax, Yax[inds[2]], yerr = Yxerr[inds[2]],  label = Ystr[inds[2]], marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    axY2.errorbar( Xax, Yax[inds[1]], yerr = Yxerr[inds[1]],  label = Ystr[inds[1]], marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
    axY1.errorbar( Xax, Yax[inds[0]], yerr = Yxerr[inds[0]], label = Ystr[inds[0]],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)

    t1 = axY1.text(0.02,0.75, Ystr[inds[0]],  color='black', transform=axY1.transAxes)
    t2 = axY2.text(0.02,0.75, Ystr[inds[1]],  color='black', transform=axY2.transAxes)
    t3 = axY3.text(0.02,0.75, Ystr[inds[2]],  color='black', transform=axY3.transAxes)
    t4 = axY4.text(0.02,0.75, Ystr[inds[3]],  color='black', transform=axY4.transAxes)
    t5 = axY5.text(0.02,0.75, Ystr[inds[4]],  color='black', transform=axY5.transAxes)

    
    # axY1.legend(loc='upper right', frameon=True)
    # axY2.legend(loc='upper right', frameon=True)
    # axY3.legend(loc='upper right',  frameon=True)
    # axY4.legend(loc='upper right', frameon=True)
    # axY5.legend(loc='upper right', frameon=True)
    
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Season_0605/PerSeason_' + Plotname +'.pdf')
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Season_0605/PerSeason_' + Plotname +'.eps')
   # plt.show()

    
df = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/MLS_UccleInterpolated_2004-2018_Dif_final_DC.csv")


# df = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/CSV_Files/MLS_UccleInterpolated_2004-2018_Dif_meanfixed.csv")
#df = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/Codes_debug/MLS_UccleInterpolated_2004-2018_Dif.csv")

df = df[df.PreLevel < 260]
df = df.reset_index()

df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['Day'] = df['Date'].dt.strftime('%j')

winter = datetime.strptime('20031221', '%Y%m%d')
spring = datetime.strptime('20030321', '%Y%m%d')
summer = datetime.strptime('20030621', '%Y%m%d')
autumn = datetime.strptime('20030921', '%Y%m%d')

daywinter = datetime.strftime(winter, '%j')
dayspring = datetime.strftime(spring, '%j')
daysummer = datetime.strftime(summer, '%j')
dayautumn = datetime.strftime(autumn, '%j')

dfwinter = df[(df.Day >= daywinter) | (df.Day < dayspring)]
dfspring = df[(df.Day >= dayspring) & (df.Day < daysummer)]
dfsummer = df[(df.Day >= daysummer) & (df.Day < dayautumn)]
dfautumn = df[(df.Day >= dayautumn) & (df.Day < daysummer)]

# dfwinter = dfwinter.reset_index()
# dfspring = dfspring.reset_index()
# dfsummer = dfsummer.reset_index()
# dfautumn = dfautumn.reset_index()


datestr = ['']*16

date_label = ['Winter','Spring','Summer','Autumn']

dfd = {}

dfd[0] =  df[(df.Day >= daywinter) | (df.Day < dayspring)]
dfd[1] = df[(df.Day >= dayspring) & (df.Day < daysummer)]
dfd[2] = df[(df.Day >= daysummer) & (df.Day < dayautumn)]
dfd[3] =  df[(df.Day >= dayautumn) & (df.Day < daywinter)]

dfd[0] = dfd[0].reset_index()
dfd[1] = dfd[1].reset_index()
dfd[2] = dfd[2].reset_index()
dfd[3] = dfd[3].reset_index()

seasonsize = 4
presize = 20
# changed for more pressure levels, presize was 15


dif_ucmean = [] ;dif_ucmedian = []; dif_ucint = []
dif_ucmean2 = [] ;dif_ucmedian2 = []; dif_ucint2 = []


rdif_ucmean = [] ; rdif_ucmedian = []; rdif_ucint = []
rdif2_ucmean = [] ; rdif2_ucmedian = []; rdif2_ucint = []


main_dif_ucmean = []; main_dif_ucmean2 = []; main_rdif_ucmean = []; main_rdif2_ucmean = []
main_dif_ucint = []; main_dif_ucint2 = []; main_rdif_ucint = []; main_rdif2_ucint = []

# always 15,15, first date then pressure index
for dd in range(seasonsize):

   # main_dif_ucmean.append([]);  main_dif_ucmean2.append([]); main_rdif_ucmean.append([]); main_rdif2_ucmean.append([])
   # main_dif_ucint.append([]);  main_dif_ucint2.append([]);main_rdif_ucint.append([]); main_rdif2_ucint.append([])

    dif_ucmean.append([]); dif_ucmedian.append([]);dif_ucint.append([])
    dif_ucmean2.append([]); dif_ucmedian2.append([]);dif_ucint2.append([])

    rdif_ucmean.append([]); rdif_ucmedian.append([]);rdif_ucint.append([])
    rdif2_ucmean.append([]); rdif2_ucmedian.append([]);rdif2_ucint.append([])
    
    for t in range(presize): 
        dif_ucmean[dd].append([]); dif_ucmedian[dd].append([]);dif_ucint[dd].append([])
        dif_ucmean2[dd].append([]); dif_ucmedian2[dd].append([]);dif_ucint2[dd].append([])

        rdif_ucmean[dd].append([]); rdif_ucmedian[dd].append([]);rdif_ucint[dd].append([])
        rdif2_ucmean[dd].append([]); rdif2_ucmedian[dd].append([]);rdif2_ucint[dd].append([])
        
        main_dif_ucmean.append([]);  main_dif_ucmean2.append([]); main_rdif_ucmean.append([]); main_rdif2_ucmean.append([])
        main_dif_ucint.append([]);  main_dif_ucint2.append([]);main_rdif_ucint.append([]); main_rdif2_ucint.append([])
    

mean_ucmean = np.zeros((seasonsize,presize)); mean_ucmedian = np.zeros((seasonsize,presize)); mean_ucint = np.zeros((seasonsize,presize))
mean_ucmean2 = np.zeros((seasonsize,presize)); mean_ucmedian2 = np.zeros((seasonsize,presize)); mean_ucint2 = np.zeros((seasonsize,presize))

mean_rucmean = np.zeros((seasonsize,presize)); mean_rucmedian = np.zeros((seasonsize,presize)); mean_rucint = np.zeros((seasonsize,presize))
mean_r2ucmean = np.zeros((seasonsize,presize)); mean_r2ucmedian = np.zeros((seasonsize,presize)); mean_r2ucint = np.zeros((seasonsize,presize))

std_ucmean = np.zeros((seasonsize,presize)); std_ucmedian = np.zeros((seasonsize,presize)); std_ucint = np.zeros((seasonsize,presize))
std_ucmean2 = np.zeros((seasonsize,presize)); std_ucmedian2 = np.zeros((seasonsize,presize)); std_ucint2 = np.zeros((seasonsize,presize))
std_rucmean = np.zeros((seasonsize,presize)); std_rucmedian = np.zeros((seasonsize,presize)); std_rucint = np.zeros((seasonsize,presize))
std_r2ucmean = np.zeros((seasonsize,presize)); std_r2ucmedian = np.zeros((seasonsize,presize)); std_r2ucint = np.zeros((seasonsize,presize))


main_mean_ucmean = np.zeros(presize); main_mean_ucmean2 = np.zeros(presize); main_mean_rucmean = np.zeros(presize); main_mean_r2ucmean = np.zeros(presize);
main_mean_ucint = np.zeros(presize); main_mean_ucint2 = np.zeros(presize); main_mean_rucint = np.zeros(presize); main_mean_r2ucint = np.zeros(presize);

main_std_ucmean = np.zeros(presize); main_std_ucmean2 = np.zeros(presize); main_std_rucmean = np.zeros(presize); main_std_r2ucmean = np.zeros(presize);
main_std_ucint = np.zeros(presize); main_std_ucint2 = np.zeros(presize); main_std_rucint = np.zeros(presize); main_std_r2ucint = np.zeros(presize);




print('first filling')

for di in range(seasonsize):
    for j in range(presize):
        for i in range(0,len(dfd[di]),presize):
            #print(di,j,i)

            dif_ucmean[di][j].append(dfd[di].at[i+j,'Dif_UcMean'])
            dif_ucmedian[di][j].append(dfd[di].at[i+j,'Dif_UcMedian'])
            dif_ucint[di][j].append(dfd[di].at[i+j,'Dif_UcIntLin'])

            dif_ucmean2[di][j].append(dfd[di].at[i+j,'Dif_UcMean2'])
            dif_ucmedian2[di][j].append(dfd[di].at[i+j,'Dif_UcMedian2'])
            dif_ucint2[di][j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])
            
            rdif_ucmean[di][j].append(dfd[di].at[i+j,'RDif_UcMean'])
            rdif_ucmedian[di][j].append(dfd[di].at[i+j,'RDif_UcMedian'])
            rdif_ucint[di][j].append(dfd[di].at[i+j,'RDif_UcIntLin'])

            rdif2_ucmean[di][j].append(dfd[di].at[i+j,'RDif_UcMean2'])
            rdif2_ucmedian[di][j].append(dfd[di].at[i+j,'RDif_UcMedian2'])
            rdif2_ucint[di][j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])

            main_dif_ucmean[j].append(dfd[di].at[i+j,'Dif_UcMean'])
            main_dif_ucmean2[j].append(dfd[di].at[i+j,'Dif_UcMean2'])
            main_rdif_ucmean[j].append(dfd[di].at[i+j,'RDif_UcMean'])
            main_rdif2_ucmean[j].append(dfd[di].at[i+j,'RDif_UcMean2'])


            main_dif_ucint[j].append(dfd[di].at[i+j,'Dif_UcIntLin'])
            main_dif_ucint2[j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])
            main_rdif_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin'])
            main_rdif2_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])


print('end of first filling')

for ld in range(presize):
    
    # for the all years
    main_mean_ucmean[ld] = np.nanmean(main_dif_ucmean[ld])
    main_mean_ucmean2[ld] = np.nanmean(main_dif_ucmean2[ld])
    main_mean_rucmean[ld] = np.nanmean(main_rdif_ucmean[ld])
    main_mean_r2ucmean[ld] = np.nanmean(main_rdif2_ucmean[ld])
    
    main_mean_ucint[ld] = np.nanmean(main_dif_ucint[ld])
    main_mean_ucint2[ld] = np.nanmean(main_dif_ucint2[ld])
    main_mean_rucint[ld] = np.nanmean(main_rdif_ucint[ld])
    main_mean_r2ucint[ld] = np.nanmean(main_rdif2_ucint[ld])

    main_std_ucmean[ld] = np.nanstd(main_dif_ucmean[ld])
    main_std_ucmean2[ld] = np.nanstd(main_dif_ucmean2[ld])
    main_std_rucmean[ld] = np.nanstd(main_rdif_ucmean[ld])
    main_std_r2ucmean[ld] = np.nanstd(main_rdif2_ucmean[ld])
    
    main_std_ucint[ld] = np.nanstd(main_dif_ucint[ld])
    main_std_ucint2[ld] = np.nanstd(main_dif_ucint2[ld])
    main_std_rucint[ld] = np.nanstd(main_rdif_ucint[ld])
    main_std_r2ucint[ld] = np.nanstd(main_rdif2_ucint[ld])
    


    for l in range(seasonsize):
        # for the indivudual years
        #print('ld', ld, 'l', l)
        mean_ucmean[l,ld] = np.nanmean(dif_ucmean[l][ld])
        mean_ucmedian[l,ld] = np.nanmean(dif_ucmedian[l][ld])
        mean_ucint[l,ld] = np.nanmean(dif_ucint[l][ld])

        mean_ucmean2[l,ld] = np.nanmean(dif_ucmean2[l][ld])
        mean_ucmedian2[l,ld] = np.nanmean(dif_ucmedian2[l][ld])
        mean_ucint2[l,ld] = np.nanmean(dif_ucint2[l][ld])

        mean_rucmean[l,ld] = np.nanmean(rdif_ucmean[l][ld])
        mean_rucmedian[l,ld] = np.nanmean(rdif_ucmedian[l][ld])
        mean_rucint[l,ld] = np.nanmean(rdif_ucint[l][ld])

        mean_r2ucmean[l,ld] = np.nanmean(rdif2_ucmean[l][ld])
        mean_r2ucmedian[l,ld] = np.nanmean(rdif2_ucmedian[l][ld])
        mean_r2ucint[l,ld] = np.nanmean(rdif2_ucint[l][ld])


        std_ucmean[l,ld] = np.nanstd(dif_ucmean[l][ld])
        std_ucmedian[l,ld] = np.nanstd(dif_ucmedian[l][ld])
        std_ucint[l,ld] = np.nanstd(dif_ucint[l][ld])

        std_ucmean2[l,ld] = np.nanstd(dif_ucmean2[l][ld])
        std_ucmedian2[l,ld] = np.nanstd(dif_ucmedian2[l][ld])
        std_ucint2[l,ld] = np.nanstd(dif_ucint2[l][ld])

        std_rucmean[l,ld] = np.nanstd(rdif_ucmean[l][ld])
        std_rucmedian[l,ld] = np.nanstd(rdif_ucmedian[l][ld])
        std_rucint[l,ld] = np.nanstd(rdif_ucint[l][ld])

        std_r2ucmean[l,ld] = np.nanstd(rdif2_ucmean[l][ld])
        std_r2ucmedian[l,ld] = np.nanstd(rdif2_ucmedian[l][ld])
        std_r2ucint[l,ld] = np.nanstd(rdif2_ucint[l][ld])
        
        

print('two')
#
Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]
#

plotyearly(mean_ucmean, std_ucmean, main_mean_ucmean, main_std_ucmean,  Y, [-5,5], date_label,
           'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_UcMean_PerSeason')
plotyearly(mean_ucint, std_ucint, main_mean_ucint, main_std_ucint,  Y, [-5,5], date_label,
           'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_UcIntLin_PerSeason')

plotyearly(mean_ucmean2, std_ucmean2, main_mean_ucmean2, main_std_ucmean2,  Y,[-5,5],  date_label,
           'MLS-Uccle (mPa)','P Air (hPa)','Dif_MLS-Uccle_UcMean_PerSeason')
plotyearly(mean_ucint2, std_ucint2, main_mean_ucint2, main_std_ucint2,  Y, [-5,5], date_label,
           'MLS-Uccle (mPa)','P Air (hPa)','Dif_MLS-Uccle_UcIntLin_PerSeason')

plotyearly(mean_rucmean, std_rucmean, main_mean_rucmean, main_std_rucmean,  Y, [-100,100], date_label,
           'Uccle-MLS (%)','P Air (hPa)','RDif_Uccle-MLS_UcMean_PerSeason')
plotyearly(mean_rucint, std_rucint, main_mean_rucint, main_std_rucint,  Y, [-100,100],date_label,
           'Uccle-MLS (%)','P Air (hPa)','RDif_Uccle-MLS_UcIntLin_PerSeason')

# plotyearly(mean_r2ucmean, std_r2ucmean, main_mean_r2ucmean, main_std_r2ucmean,  Y,[-100,100], date_label, 'MLS-Uccle (%)','P Air (hPa)','RDif_MLS-Uccle_UcMean_PerSeason')
# plotyearly(mean_r2ucint, std_r2ucint, main_mean_r2ucint, main_std_r2ucint,  Y, [-100,100], date_label, 'Uccle-MLS (%)','P Air (hPa)','RDif_MLS-Uccle_UcIntLin_PerSeason')

plotyearly(mean_r2ucmean, std_r2ucmean, main_mean_r2ucmean, main_std_r2ucmean,  Y,[-25,75], date_label,
           'MLS-Uccle (%)','P Air (hPa)','RDif_MLS-Uccle_UcMean_PerYear')
plotyearly(mean_r2ucint, std_r2ucint, main_mean_r2ucint, main_std_r2ucint,  Y, [-40,60], date_label,
           'MLS-Uccle (%)','P Air (hPa)','RDif_MLS-Uccle_UcIntLin_PerYear')
plotyearly(mean_r2ucint, std_r2ucint, main_mean_r2ucint, main_std_r2ucint,  Y, [-20,30], date_label,
           'MLS-Uccle (%)','P Air (hPa)','ZoomRDif_MLS-Uccle_UcIntLin_PerYear')
plotyearly(mean_r2ucint, std_r2ucint, main_mean_r2ucint, main_std_r2ucint,  Y, [-60,60], date_label,
           'MLS-Uccle (%)','P Air (hPa)','2RDif_MLS-Uccle_UcIntLin_PerYear')



### The part for yearly subplots
Xseason = ['Winter', 'Spring','Summer','Autumn']

y_mean_ucmean2 = []; y_mean_ucint2 = []; y_mean_r2ucmean = []; y_mean_r2ucint = []
y_std_ucmean2 = []; y_std_ucint2 = []; y_std_r2ucmean = []; y_std_r2ucint = []

Ystr = [''] * presize


for xx in range(presize):
    y_mean_ucmean2.append([]); y_mean_ucint2.append([]); y_mean_r2ucmean.append([]); y_mean_r2ucint.append([]);
    y_std_ucmean2.append([]); y_std_ucint2.append([]); y_std_r2ucmean.append([]); y_std_r2ucint.append([]);
    Ystr[xx] = str(Y[xx])+' hPa'

for ix in range(presize):
    for iy in range(seasonsize):
        y_mean_ucmean2[ix].append(mean_ucmean2[iy][ix])
        y_mean_ucint2[ix].append(mean_ucint2[iy][ix])
        y_mean_r2ucmean[ix].append(mean_r2ucmean[iy][ix])
        y_mean_r2ucint[ix].append(mean_r2ucint[iy][ix])

        y_std_ucmean2[ix].append(std_ucmean2[iy][ix])
        y_std_ucint2[ix].append(std_ucint2[iy][ix])
        y_std_r2ucmean[ix].append(std_r2ucmean[iy][ix])
        y_std_r2ucint[ix].append(std_r2ucint[iy][ix])
        
        
print('y mean ucint [0]' , y_mean_ucmean2[0] )
print('test', mean_ucmean2[0][0],  mean_ucmean2[1][0],  mean_ucmean2[2][0],  mean_ucmean2[3][0])

##pre levels Y = [ 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678]
#option 1

# plotmeanyearlyOpOne(Xseason,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_UcMean_215-100',[0,1,2,3,4],[-3,3])
# plotmeanyearlyOpOne(Xseason,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_UcMean_82-38',[5,6,7,8,9],[-3,3])
# plotmeanyearlyOpOne(Xseason,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_UcMean_31-14',[10,11,12,13,14],[-3,3])
#
# plotmeanyearlyOpOne(Xseason,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_215-100',[0,1,2,3,4],[-3,3])
# plotmeanyearlyOpOne(Xseason,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_82-38',[5,6,7,8,9],[-3,3])
# plotmeanyearlyOpOne(Xseason,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_31-14',[10,11,12,13,14],[-3,3])
#
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_UcMean_215-100',[0,1,2,3,4],[-60,60])
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_UcMean_82-38',[5,6,7,8,9],[-30,30])
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_UcMean_31-14',[10,11,12,13,14],[-20,20])
#
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_215-100',[0,1,2,3,4],[-60,60])
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_82-38',[5,6,7,8,9],[-30,30])
# plotmeanyearlyOpOne(Xseason,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_31-14',[10,11,12,13,14],[-20,20])




# second option


# ax5 = plt.subplot(515)
# ax5.errorbar( Xyear, y_mean_ucmean2[0], yerr = std_ucint[0], label = Ystr[0],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
# ax4 = plt.subplot(514)
# ax4.errorbar( Xyear, y_mean_ucmean2[1], yerr = std_ucint[1], label = Ystr[1],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
# ax3 = plt.subplot(513)
# ax3.errorbar( Xyear, y_mean_ucmean2[2], yerr = std_ucint[2], label = Ystr[2],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
# ax2 = plt.subplot(512)
# ax2.errorbar( Xyear, y_mean_ucmean2[3], yerr = std_ucint[3], label = Ystr[3],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)
# ax1 = plt.subplot(511)
# ax1.errorbar( Xyear, y_mean_ucmean2[4], yerr = std_ucint[4], label = Ystr[4],  marker = "o",  linewidth = 0.5, elinewidth = 0.5, capsize = 4, capthick=1.0)

# ax1.legend(loc='upper right', frameon=True)
# ax2.legend(loc='upper right', frameon=True)
# ax3.legend(loc='upper right')
# ax4.legend(loc='upper right', frameon=True)
# ax5.legend(loc='upper right', frameon=True)
# plt.show()
