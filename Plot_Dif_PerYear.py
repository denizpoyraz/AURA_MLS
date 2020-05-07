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


def plotyearly(xarray,std_xarray,main_xarray,std_main_xarray,Yax,xranges,plotlabel,xtitle,ytitle,plotname):
    # def plotyearly(mean_ucint, std_ucint, Y, date_label, 'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_UcIntLinPerYear'):

    fig,ax0=plt.subplots()
    plt.ylim(250,3)
    plt.xlim(xranges)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    ax0.tick_params(axis='both',which='both',direction='in')
    ax0.yaxis.set_ticks_position('both')
    ax0.xaxis.set_ticks_position('both')
    ax0.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.set_yscale('log')
    ax0.axvline(x=0,color='grey',linestyle='--')

    plt.plot(xarray[0],Yax,label=plotlabel[0],linewidth=0.5,marker="o")
    plt.plot(xarray[1],Yax,label=plotlabel[1],linewidth=0.5,marker="v")
    plt.plot(xarray[2],Yax,label=plotlabel[2],linewidth=0.5,marker="^")
    plt.plot(xarray[3],Yax,label=plotlabel[3],linewidth=0.5,marker="<")
    plt.plot(xarray[4],Yax,label=plotlabel[4],linewidth=0.5,marker=">")
    plt.plot(xarray[5],Yax,label=plotlabel[5],linewidth=0.5,marker="8")
    plt.plot(xarray[6],Yax,label=plotlabel[6],linewidth=0.5,marker="s")
    plt.plot(xarray[7],Yax,label=plotlabel[7],linewidth=0.5,marker="p")
    plt.plot(xarray[8],Yax,label=plotlabel[8],linewidth=0.5,marker="P")
    plt.plot(xarray[9],Yax,label=plotlabel[9],linewidth=0.5,marker="h")
    plt.plot(xarray[10],Yax,label=plotlabel[10],linewidth=0.5,marker="X")
    plt.plot(xarray[11],Yax,label=plotlabel[11],linewidth=0.5,marker="D")
    plt.plot(xarray[12],Yax,label=plotlabel[12],linewidth=0.5,marker="d")
    plt.plot(xarray[13],Yax,label=plotlabel[13],linewidth=0.5,marker="*")
    plt.plot(xarray[14],Yax,label=plotlabel[14],linewidth=0.5,marker="X")

    ax0.set_yticks([200,160,120,100,80,70,60,50,40,30,20,15,10,5])
    plt.ylim(250,4)

    ax0.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678

    ax0.errorbar(main_xarray,Yax,xerr=std_main_xarray,label='All',marker="x",color='black',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)

    std_p5 = [i + 5 for i in main_xarray]
    std_m5 = [i - 5 for i in main_xarray]

    print(std_main_xarray)
    print(main_xarray)
    print(std_p5)
    ax0.legend(loc='upper right',frameon=True,fontsize='x-small')

    ax0.axvspan(-5, 5, alpha=0.2, color='grey')
    # ax0.fill_between(std_m5, std_p5, 1)
    # ax0.fill_betweenx(Yax,  std_m5, std_p5, alpha=0.2, facecolor='k')

    # ax0.axvspan(-5, 5, alpha=0.2, color='grey')

    #    #
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/' + plotname + 'v1.pdf')
    plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/' + plotname + 'v1.eps')
    #
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Dif_UcIntLinPerYear.pdf')
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots/Plots_timenight/Dif_UcIntLinPerYear.eps')

    plt.show()

#######################################################################################################################
# #######################################

df=pd.read_csv("/home/poyraden/Analysis/AURA_MLS/MLS_UccleInterpolated_2004-2018_Dif_final_DC.csv")
# df = pd.read_csv("/home/poyraden/Analysis/AURA_MLS/Codes/MLS_UccleInterpolated_2004-2018_Dif.csv")

# df = df[df.PreLevel < 217]
df=df[df.PreLevel <= 260]
# df = df[(df.Date < 20170101) | (df.Date > 20173112)]

## check for years



# ''' extra condition to select only noon-night hours'''
#
# df['Time'] = pd.to_datetime(df['Time'],format= '%H:%M:%S' ).dt.time
# df = df[df.Time > time(6,0,0)]
#
# '''                '''


df=df.reset_index()

df['Date']=pd.to_datetime(df['Date'],format='%Y%m%d')

df['Year'] = pd.DatetimeIndex(df['Date']).year

# df = df[df.Year < 2006]

datestr=[''] * 16

date_label=[''] * 16

dfd={}

# to bi fixed: replace 15 with datsize and 17 with prelevelsize


for d in range(2004,2020):
    i=d - 2004
    datestr[i]=datetime(d,1,1)
    date_label[i]=str(d)
    print(i,d,datestr[i])

datesize=15
presize=20

for dj in range(datesize):
    dfd[dj]=df[(df.Date >= datestr[dj]) & (df.Date < datestr[dj + 1])]
    dfd[dj] = dfd[dj].reset_index()

dif_ucmean=[];
dif_ucmedian=[];
dif_ucint=[]
dif_ucmean2=[];
dif_ucmedian2=[];
dif_ucint2=[]

rdif_ucmean=[];
rdif_ucmedian=[];
rdif_ucint=[]
rdif2_ucmean=[];
rdif2_ucmedian=[];
rdif2_ucint=[]

main_dif_ucmean=[];
main_dif_ucmean2=[];
main_rdif_ucmean=[];
main_rdif2_ucmean=[]
main_dif_ucint=[];
main_dif_ucint2=[];
main_rdif_ucint=[];
main_rdif2_ucint=[]

# always 15,15, first date then pressure index
for dd in range(datesize):

    dif_ucmean.append([]);
    dif_ucmedian.append([]);
    dif_ucint.append([])
    dif_ucmean2.append([]);
    dif_ucmedian2.append([]);
    dif_ucint2.append([])

    rdif_ucmean.append([]);
    rdif_ucmedian.append([]);
    rdif_ucint.append([])
    rdif2_ucmean.append([]);
    rdif2_ucmedian.append([]);
    rdif2_ucint.append([])

    for t in range(presize):
        dif_ucmean[dd].append([]);
        dif_ucmedian[dd].append([]);
        dif_ucint[dd].append([])
        dif_ucmean2[dd].append([]);
        dif_ucmedian2[dd].append([]);
        dif_ucint2[dd].append([])

        rdif_ucmean[dd].append([]);
        rdif_ucmedian[dd].append([]);
        rdif_ucint[dd].append([])
        rdif2_ucmean[dd].append([]);
        rdif2_ucmedian[dd].append([]);
        rdif2_ucint[dd].append([])

        main_dif_ucmean.append([]);
        main_dif_ucmean2.append([]);
        main_rdif_ucmean.append([]);
        main_rdif2_ucmean.append([])
        main_dif_ucint.append([]);
        main_dif_ucint2.append([]);
        main_rdif_ucint.append([]);
        main_rdif2_ucint.append([])

mean_ucmean=np.zeros((datesize,presize));
mean_ucmedian=np.zeros((datesize,presize));
mean_ucint=np.zeros((datesize,presize))
mean_ucmean2=np.zeros((datesize,presize));
mean_ucmedian2=np.zeros((datesize,presize));
mean_ucint2=np.zeros((datesize,presize))

mean_rucmean=np.zeros((datesize,presize));
mean_rucmedian=np.zeros((datesize,presize));
mean_rucint=np.zeros((datesize,presize))
mean_r2ucmean=np.zeros((datesize,presize));
mean_r2ucmedian=np.zeros((datesize,presize));
mean_r2ucint=np.zeros((datesize,presize))

main_mean_ucmean=np.zeros(presize);
main_mean_ucmean2=np.zeros(presize);
main_mean_rucmean=np.zeros(presize);
main_mean_r2ucmean=np.zeros(presize);
main_mean_ucint=np.zeros(presize);
main_mean_ucint2=np.zeros(presize);
main_mean_rucint=np.zeros(presize);
main_mean_r2ucint=np.zeros(presize);

main_std_ucmean=np.zeros(presize);
main_std_ucmean2=np.zeros(presize);
main_std_rucmean=np.zeros(presize);
main_std_r2ucmean=np.zeros(presize);
main_std_ucint=np.zeros(presize);
main_std_ucint2=np.zeros(presize);
main_std_rucint=np.zeros(presize);
main_std_r2ucint=np.zeros(presize);

std_ucmean=np.zeros((datesize,presize));
std_ucmedian=np.zeros((datesize,presize));
std_ucint=np.zeros((datesize,presize))
std_ucmean2=np.zeros((datesize,presize));
std_ucmedian2=np.zeros((datesize,presize));
std_ucint2=np.zeros((datesize,presize))
std_rucmean=np.zeros((datesize,presize));
std_rucmedian=np.zeros((datesize,presize));
std_rucint=np.zeros((datesize,presize))
std_r2ucmean=np.zeros((datesize,presize));
std_r2ucmedian=np.zeros((datesize,presize));
std_r2ucint=np.zeros((datesize,presize))

print('first filling')

print(datesize, presize)

for di in range(datesize):
    for j in range(presize):
        for i in range(0,len(dfd[di]),presize):
            # print(di,j,i)
            # print(di,i, j, 'dfd[di].at[i+j,RDif_UcMean2]', dfd[di].loc[i+j]['RDif_UcMean2'])
            #
            # print(di,i, j, 'dfd[di].at[i+j,RDif_UcMean2]', dfd[di].at[i+j,'RDif_UcMean2'])
            # print(di,i, j, 'dfd[di].at[i+j,RDif_UcMean2]', dfd[di].at[i+j, 'RDif_UcMean2'])


            # print(di,i, j, 'dfd[di].at[i+j,Dif_UcMean]', dfd[di].at[i+j,'Dif_UcMean'])

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

            # main_dif_ucint[j].append(dfd[di].at[i+j,'Dif_UcIntLin'])
            # main_dif_ucint2[j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])
            # main_rdif_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin'])
            # main_rdif2_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])
            t = int(i+j)
            # print('i+j', t)
            main_dif_ucint[j].append(dfd[di].at[t,'Dif_UcIntLin'])
            main_dif_ucint2[j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])
            main_rdif_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin'])
            main_rdif2_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])



print('here 0 ', len(main_rdif2_ucint[0]), np.nanmean(main_rdif2_ucint[0]), main_rdif2_ucint[0])
print('here 1', len(main_rdif2_ucint[1]), np.nanmean(main_rdif2_ucint[1]), main_rdif2_ucint[1])

print('end of first filling')
## testing
print('dif_ucmean[0]',len(dif_ucmean))

for ld in range(presize):
    # for the all years
    main_mean_ucmean[ld]=np.nanmean(main_dif_ucmean[ld])
    main_mean_ucmean2[ld]=np.nanmean(main_dif_ucmean2[ld])
    main_mean_rucmean[ld]=np.nanmean(main_rdif_ucmean[ld])
    main_mean_r2ucmean[ld]=np.nanmean(main_rdif2_ucmean[ld])

    main_mean_ucint[ld]=np.nanmean(main_dif_ucint[ld])
    main_mean_ucint2[ld]=np.nanmean(main_dif_ucint2[ld])
    main_mean_rucint[ld]=np.nanmean(main_rdif_ucint[ld])
    main_mean_r2ucint[ld]=np.nanmean(main_rdif2_ucint[ld])

    main_std_ucmean[ld]=np.nanstd(main_dif_ucmean[ld])
    main_std_ucmean2[ld]=np.nanstd(main_dif_ucmean2[ld])
    main_std_rucmean[ld]=np.nanstd(main_rdif_ucmean[ld])
    main_std_r2ucmean[ld]=np.nanstd(main_rdif2_ucmean[ld])

    main_std_ucint[ld]=np.nanstd(main_dif_ucint[ld])
    main_std_ucint2[ld]=np.nanstd(main_dif_ucint2[ld])
    main_std_rucint[ld]=np.nanstd(main_rdif_ucint[ld])
    main_std_r2ucint[ld]=np.nanstd(main_rdif2_ucint[ld])

    # print(ld, ' main_mean_ucint[ld]',  main_mean_ucint2[ld])
    # print(ld, '  main_mean_r2ucint[ld]',   main_mean_r2ucint[ld])

    for l in range(datesize):
        # for the indivudual years

        mean_ucmean[l,ld]=np.nanmean(dif_ucmean[l][ld])
        mean_ucmedian[l,ld]=np.nanmean(dif_ucmedian[l][ld])
        mean_ucint[l,ld]=np.nanmean(dif_ucint[l][ld])

        mean_ucmean2[l,ld]=np.nanmean(dif_ucmean2[l][ld])
        mean_ucmedian2[l,ld]=np.nanmean(dif_ucmedian2[l][ld])
        # np.NaN if np.all(b!=b) else np.nanmean(b)
        mean_ucint2[l,ld]=np.NaN if (dif_ucmedian2[l][ld] != dif_ucmedian2[l][ld]) else np.nanmean(dif_ucint2[l][ld])

        # mean_ucint2[l,ld] = np.nanmean(dif_ucint2[l][ld])

        mean_rucmean[l,ld]=np.nanmean(rdif_ucmean[l][ld])
        mean_rucmedian[l,ld]=np.nanmean(rdif_ucmedian[l][ld])
        mean_rucint[l,ld]=np.nanmean(rdif_ucint[l][ld])

        mean_r2ucmean[l,ld]=np.nanmean(rdif2_ucmean[l][ld])
        mean_r2ucmedian[l,ld]=np.nanmean(rdif2_ucmedian[l][ld])
        # mean_r2ucint[l,ld] = np.nanmean(rdif2_ucint[l][ld])
        mean_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanmean(rdif2_ucint[l][ld])

        std_ucmean[l,ld]=np.nanstd(dif_ucmean[l][ld])
        std_ucmedian[l,ld]=np.nanstd(dif_ucmedian[l][ld])
        std_ucint[l,ld]=np.nanstd(dif_ucint[l][ld])

        std_ucmean2[l,ld]=np.nanstd(dif_ucmean2[l][ld])
        std_ucmedian2[l,ld]=np.nanstd(dif_ucmedian2[l][ld])
        std_ucint2[l,ld]=np.nanstd(dif_ucint2[l][ld])

        std_rucmean[l,ld]=np.nanstd(rdif_ucmean[l][ld])
        std_rucmedian[l,ld]=np.nanstd(rdif_ucmedian[l][ld])
        std_rucint[l,ld]=np.nanstd(rdif_ucint[l][ld])

        std_r2ucmean[l,ld]=np.nanstd(rdif2_ucmean[l][ld])
        std_r2ucmedian[l,ld]=np.nanstd(rdif2_ucmedian[l][ld])
        # std_r2ucint[l,ld] = np.nanstd(rdif2_ucint[l][ld])
        std_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanstd(rdif2_ucint[l][ld])
#

# print(' V2  0th entry, pressure 216' , main_rdif2_ucint[0], 'main_mean_r2ucint ',   main_mean_r2ucint)


print('two')

#
Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]
#


# print('ADif noon mean interpolated')
# print(*main_mean_ucint, sep = ', ')
# print('ADif noon mean interpolated err')
# print(*main_std_ucint, sep = ',' )
#
# print('RDif noon mean interpolated')
# print(*main_mean_r2ucint, sep = ',' )
# print('RDif noon mean interpolated err')
# print(*main_std_r2ucint, sep = ',' )


# plotyearly(mean_ucmean,std_ucmean,main_mean_ucmean,main_std_ucmean,Y,[-3,3],date_label,
#            'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_Mean_PerYear')
# plotyearly(mean_ucint,std_ucint,main_mean_ucint,main_std_ucint,Y,[-3,3],date_label,
#            'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_IntLin_PerYear')
#
# plotyearly(mean_ucmean2,std_ucmean2,main_mean_ucmean2,main_std_ucmean2,Y,[-3,3],date_label,
#            'MLS-Uccle (mPa)','P Air (hPa)','Dif_MLS-Uccle_Mean_PerYear')
# plotyearly(mean_ucint2,std_ucint2,main_mean_ucint2,main_std_ucint2,Y,[-3,3],date_label,
#            'MLS-Uccle (mPa)','P Air (hPa)','Dif_MLS-Uccle_IntLin_PerYear')
#
# plotyearly(mean_rucmean,std_rucmean,main_mean_rucmean,main_std_rucmean,Y,[-100,100],date_label,
#            'Uccle-MLS (%)','P Air (hPa)','RDif_Uccle-MLS_Mean_PerYear')
# plotyearly(mean_rucint,std_rucint,main_mean_rucint,main_std_rucint,Y,[-100,100],date_label,
#            'Uccle-MLS (%)','P Air (hPa)','RDif_Uccle-MLS_IntLin_PerYear')

# plotyearly(mean_r2ucmean,std_r2ucmean,main_mean_r2ucmean,main_std_r2ucmean,Y,[-60,80],date_label,
#            'MLS-Uccle (%)','P Air (hPa)','RDif_MLS-Uccle_Mean_PerYear')
# plotyearly(mean_r2ucmedian,std_r2ucmedian,main_mean_r2ucmedian,main_std_r2ucmedian,Y,[-60,80],date_label,
#            'MLS-Uccle (%) median','P Air (hPa)','RDif_MLS-Uccle_Mean_PerYear')
# plotyearly(mean_r2ucint,std_r2ucint,main_mean_r2ucint,main_std_r2ucint,Y,[-40,40],date_label,
#            'MLS-Uccle (%)','P Air (hPa)','RDif_MLS-Uccle_IntLin_PerYear')
# plotyearly(mean_r2ucint,std_r2ucint,main_mean_r2ucint,main_std_r2ucint,Y,[-20,20],date_label,
#            'MLS-Uccle (%)','P Air (hPa)','ZoomRDif_MLS-Uccle_IntLin_PerYear')

print('mean_r2ucint 0', mean_r2ucint[0][0])
print('std_r2ucint 0', std_r2ucint[0][0])
print('mean_r2ucint 1', mean_r2ucint[1][0])
print('std_r2ucint 1', std_r2ucint[1][0])
print('main_mean_r2ucint', main_mean_r2ucint[0:2])
print('main_std_r2ucint', main_std_r2ucint[0:2])

plotyearly(mean_r2ucint,std_r2ucint,main_mean_r2ucint,main_std_r2ucint,Y,[-60,60],date_label,
           'MLS-Uccle (%)','P Air (hPa)','RDif2_MLS-Uccle_IntLin_PerYear_DC')



# ### The part for yearly subplots
# Xyear = []
#
# y_mean_ucmean2 = []; y_mean_ucint2 = []; y_mean_r2ucmean = []; y_mean_r2ucint = []
# y_std_ucmean2 = []; y_std_ucint2 = []; y_std_r2ucmean = []; y_std_r2ucint = []
#
# Ystr = [''] * presize
#
# for yy in range(2004, 2019):
#     Xyear.append(yy)
#
# for xx in range(presize):
#     y_mean_ucmean2.append([]); y_mean_ucint2.append([]); y_mean_r2ucmean.append([]); y_mean_r2ucint.append([]);
#     y_std_ucmean2.append([]); y_std_ucint2.append([]); y_std_r2ucmean.append([]); y_std_r2ucint.append([]);
#     Ystr[xx] = str(Y[xx])+' hPa'
#
# for ix in range(presize):
#     for iy in range(datesize):
#         y_mean_ucmean2[ix].append(mean_ucmean2[iy][ix])
#         y_mean_ucint2[ix].append(mean_ucint2[iy][ix])
#         y_mean_r2ucmean[ix].append(mean_r2ucmean[iy][ix])
#         y_mean_r2ucint[ix].append(mean_r2ucint[iy][ix])
#
#         y_std_ucmean2[ix].append(std_ucmean2[iy][ix])
#         y_std_ucint2[ix].append(std_ucint2[iy][ix])
#         y_std_r2ucmean[ix].append(std_r2ucmean[iy][ix])
#         y_std_r2ucint[ix].append(std_r2ucint[iy][ix])
#
#
# plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_Mean_215-100',[0,1,2,3,4],[-3,3],'Dif')
# plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_Mean_82-38',[5,6,7,8,9],[-2,2],'Dif')
# plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucmean2, Ystr, 'Dif_Mean_31-14',[10,11,12,13,14],[-1.5,1.5],'Dif')
#
# plotmeanyearlyOpOne(Xyear,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_215-100',[0,1,2,3,4],[-3,3],'Dif')
# plotmeanyearlyOpOne(Xyear,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_82-38',[5,6,7,8,9],[-2,2],'Dif')
# plotmeanyearlyOpOne(Xyear,  y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt_31-14',[10,11,12,13,14],[-1.5,1.5],'Dif')
#
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_Mean_215-100',[0,1,2,3,4],[-60,60],'RDif')
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_Mean_82-38',[5,6,7,8,9],[-20,20],'RDif')
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucmean,  y_std_r2ucmean, Ystr, 'RDif_Mean_31-14',[10,11,12,13,14],[-10,10],'RDif')
#
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_215-100',[0,1,2,3,4],[-60,60],'RDif')
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_82-38',[5,6,7,8,9],[-20,30],'RDif')
# plotmeanyearlyOpOne(Xyear,  y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt_31-14',[10,11,12,13,14],[-10,10],'RDif')
#
#
#
# plotmeanyearlyReduced(Xyear, y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt',[2,5,8,10,14],[-4,4,-4,4,-3,3,-2,2,-2,2],'Dif')
# plotmeanyearlyReduced(Xyear, y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt',[2,5,8,10,14],[-80,80,-40,40,-35,35,-25,25,-25,25],'RDif')


##########################################


#
# def plotmeanyearlyOpOne(Xax,Yax,Yxerr,PreLabel,Plotname,inds,ylimit,keyword):
#     # plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucint2, Ystr, 'Dif_UcMean_215-100',[0,1,2,3,4])
#
#     figY=plt.figure()
#
#     axY5=figY.add_axes([0.1,0.7,0.8,0.15])
#     axY4=figY.add_axes([0.1,0.55,0.8,0.15])
#     axY3=figY.add_axes([0.1,0.4,0.8,0.15])
#     axY2=figY.add_axes([0.1,0.25,0.8,0.15])
#     axY1=figY.add_axes([0.1,0.1,0.8,0.15])
#
#     if (keyword == 'Dif'):
#         axY5.set_title('Yearly Mean MLS-Uccle')
#         # axY1.set_ylabel('MLS-Uccle (mPa)')
#         # axY2.set_ylabel('MLS-Uccle (mPa)')
#         axY3.set_ylabel('MLS-Uccle (mPa)')
#         # axY4.set_ylabel('MLS-Uccle (mPa)')
#         # axY5.set_ylabel('MLS-Uccle (mPa)')
#
#     if (keyword == 'RDif'):
#         axY5.set_title('Yearly Relative Mean MLS-Uccle')
#         # axY1.set_ylabel('MLS-Uccle (%)')
#         # axY2.set_ylabel('MLS-Uccle (%)')
#         axY3.set_ylabel('MLS-Uccle (%)')
#         # axY4.set_ylabel('MLS-Uccle (%)')
#         # axY5.set_ylabel('MLS-Uccle (%)')
#
#     axY1.set_ylim(ylimit)
#     axY2.set_ylim(ylimit)
#     axY3.set_ylim(ylimit)
#     axY4.set_ylim(ylimit)
#     axY5.set_ylim(ylimit)
#
#     axY5.tick_params(axis='both',which='both',direction='in')
#     axY5.yaxis.set_ticks_position('both')
#     axY5.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY4.tick_params(axis='both',which='both',direction='in')
#     axY5.yaxis.set_ticks_position('both')
#     axY4.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY3.tick_params(axis='both',which='both',direction='in')
#     axY3.yaxis.set_ticks_position('both')
#     axY3.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY2.tick_params(axis='both',which='both',direction='in')
#     axY2.yaxis.set_ticks_position('both')
#     axY2.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY1.tick_params(axis='both',which='both',direction='in')
#     axY1.yaxis.set_ticks_position('both')
#     axY1.yaxis.set_minor_locator(AutoMinorLocator(10))
#
#     axY5.errorbar(Xax,Yax[inds[4]],yerr=Yxerr[inds[4]],label=Ystr[inds[4]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY4.errorbar(Xax,Yax[inds[3]],yerr=Yxerr[inds[3]],label=Ystr[inds[3]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY3.errorbar(Xax,Yax[inds[2]],yerr=Yxerr[inds[2]],label=Ystr[inds[2]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY2.errorbar(Xax,Yax[inds[1]],yerr=Yxerr[inds[1]],label=Ystr[inds[1]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY1.errorbar(Xax,Yax[inds[0]],yerr=Yxerr[inds[0]],label=Ystr[inds[0]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#
#     Xax=np.array(Xax)
#     for p in range(5):
#         Yax[inds[p]]=np.array(Yax[inds[p]])
#
#     fit1=np.polyfit(Xax,Yax[inds[0]],1)
#     fit1_fn=np.poly1d(fit1)
#     fit2=np.polyfit(Xax,Yax[inds[1]],1)
#     fit2_fn=np.poly1d(fit2)
#     fit3=np.polyfit(Xax,Yax[inds[2]],1)
#     fit3_fn=np.poly1d(fit3)
#     fit4=np.polyfit(Xax,Yax[inds[3]],1)
#     fit4_fn=np.poly1d(fit4)
#     fit5=np.polyfit(Xax,Yax[inds[4]],1)
#     fit5_fn=np.poly1d(fit5)
#
#     axY5.plot(Xax,fit5_fn(Xax),color='grey',linestyle='--',linewidth=1.5)
#     axY4.plot(Xax,fit4_fn(Xax),color='grey',linestyle='--',linewidth=1.5)
#     axY3.plot(Xax,fit3_fn(Xax),color='grey',linestyle='--',linewidth=1.5)
#     axY2.plot(Xax,fit2_fn(Xax),color='grey',linestyle='--',linewidth=1.5)
#     axY1.plot(Xax,fit1_fn(Xax),color='grey',linestyle='--',linewidth=1.5)
#
#     t1=axY1.text(0.02,0.75,Ystr[inds[0]],color='black',transform=axY1.transAxes)
#     t2=axY2.text(0.02,0.75,Ystr[inds[1]],color='black',transform=axY2.transAxes)
#     t3=axY3.text(0.02,0.75,Ystr[inds[2]],color='black',transform=axY3.transAxes)
#     t4=axY4.text(0.02,0.75,Ystr[inds[3]],color='black',transform=axY4.transAxes)
#     t5=axY5.text(0.02,0.75,Ystr[inds[4]],color='black',transform=axY5.transAxes)
#
#     # axY1.legend(loc='upper right', frameon=True)
#     # axY2.legend(loc='upper right', frameon=True)
#     # axY3.legend(loc='upper right',  frameon=True)
#     # axY4.legend(loc='upper right', frameon=True)
#     # axY5.legend(loc='upper right', frameon=True)
#
#     plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Trend_' + Plotname + '.pdf')
#     plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Trend_' + Plotname + '.eps')
#
#
# # plt.show()

# def plotmeanyearlyReduced(Xax,Yax,Yxerr,PreLabel,Plotname,inds,ylimit,keyword):
#     # plotmeanyearlyOpOne(Xyear,  y_mean_ucmean2,  y_std_ucint2, Ystr, 'Dif_UcMean_215-100',[0,1,2,3,4])
#
#     figY=plt.figure()
#
#     axY5=figY.add_axes([0.1,0.7,0.8,0.15])
#     axY4=figY.add_axes([0.1,0.55,0.8,0.15])
#     axY3=figY.add_axes([0.1,0.4,0.8,0.15])
#     axY2=figY.add_axes([0.1,0.25,0.8,0.15])
#     axY1=figY.add_axes([0.1,0.1,0.8,0.15])
#
#     if (keyword == 'Dif'):
#         axY5.set_title('Yearly Mean MLS-Uccle')
#         # axY1.set_ylabel('MLS-Uccle (mPa)')
#         # axY2.set_ylabel('MLS-Uccle (mPa)')
#         axY3.set_ylabel('MLS-Uccle (mPa)')
#         # axY4.set_ylabel('MLS-Uccle (mPa)')
#         # axY5.set_ylabel('MLS-Uccle (mPa)')
#         axY5.set_yticks([0.5,0,-0.5])
#         axY4.set_yticks([0.75,0,-0.75])
#         axY3.set_yticks([1.0,0,-1.0])
#         axY2.set_yticks([2.0,0,-2.0])
#         axY1.set_yticks([2.0,0,-2.0])
#
#         # plotmeanyearlyReduced(Xyear, y_mean_ucint2,  y_std_ucint2, Ystr, 'Dif_UcInt',[2,5,8,10,14],[-3,3,-3,3,-2,2,-1.5,1.5,-1,1],'Dif')
#         # plotmeanyearlyReduced(Xyear, y_mean_r2ucint,  y_std_r2ucint, Ystr, 'RDif_UcInt',[2,5,8,10,14],[-80,80,-40,40,-25,25,-20,20,-20,20],'RDif')
#
#     if (keyword == 'RDif'):
#         axY5.set_title('Yearly Relative Mean MLS-Uccle')
#         # axY1.set_ylabel('MLS-Uccle (%)')
#         # axY2.set_ylabel('MLS-Uccle (%)')
#         axY3.set_ylabel('MLS-Uccle (%)')
#         # axY4.set_ylabel('MLS-Uccle (%)')
#         # axY5.set_ylabel('MLS-Uccle (%)')
#         axY5.set_yticks([10,0,-10])
#         axY4.set_yticks([10,0,-10])
#         axY3.set_yticks([20,0,-20])
#         axY2.set_yticks([30,0,-30])
#         axY1.set_yticks([50,0,-50])
#
#     axY1.set_ylim(ylimit[0],ylimit[1])
#     axY2.set_ylim(ylimit[2],ylimit[3])
#     axY3.set_ylim(ylimit[4],ylimit[5])
#     axY4.set_ylim(ylimit[6],ylimit[7])
#     axY5.set_ylim(ylimit[8],ylimit[9])
#
#     axY5.tick_params(axis='both',which='both',direction='in')
#     axY5.yaxis.set_ticks_position('both')
#     axY5.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY4.tick_params(axis='both',which='both',direction='in')
#     axY5.yaxis.set_ticks_position('both')
#     axY4.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY3.tick_params(axis='both',which='both',direction='in')
#     axY3.yaxis.set_ticks_position('both')
#     axY3.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY2.tick_params(axis='both',which='both',direction='in')
#     axY2.yaxis.set_ticks_position('both')
#     axY2.yaxis.set_minor_locator(AutoMinorLocator(10))
#     axY1.tick_params(axis='both',which='both',direction='in')
#     axY1.yaxis.set_ticks_position('both')
#     axY1.yaxis.set_minor_locator(AutoMinorLocator(10))
#
#     axY5.errorbar(Xax,Yax[inds[4]],yerr=Yxerr[inds[4]],label=Ystr[inds[4]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY4.errorbar(Xax,Yax[inds[3]],yerr=Yxerr[inds[3]],label=Ystr[inds[3]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY3.errorbar(Xax,Yax[inds[2]],yerr=Yxerr[inds[2]],label=Ystr[inds[2]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY2.errorbar(Xax,Yax[inds[1]],yerr=Yxerr[inds[1]],label=Ystr[inds[1]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#     axY1.errorbar(Xax,Yax[inds[0]],yerr=Yxerr[inds[0]],label=Ystr[inds[0]],marker="o",
#                   linewidth=0.5,elinewidth=0.5,capsize=4,capthick=1.0)
#
#     axY1.axhline(y=0,color='grey',linestyle='--')
#     axY2.axhline(y=0,color='grey',linestyle='--')
#     axY3.axhline(y=0,color='grey',linestyle='--')
#     axY4.axhline(y=0,color='grey',linestyle='--')
#     axY5.axhline(y=0,color='grey',linestyle='--')
#
#     # Xax = np.array(Xax)
#     # for p in range(5):
#     #     Yax[inds[p]] = np.array(Yax[inds[p]])
#
#     # fit1 = np.polyfit(Xax, Yax[inds[0]], 1)
#     # fit1_fn = np.poly1d(fit1)
#     # fit2 = np.polyfit(Xax, Yax[inds[1]], 1)
#     # fit2_fn = np.poly1d(fit2)
#     # fit3 = np.polyfit(Xax, Yax[inds[2]], 1)
#     # fit3_fn = np.poly1d(fit3)
#     # fit4 = np.polyfit(Xax, Yax[inds[3]], 1)
#     # fit4_fn = np.poly1d(fit4)
#     # fit5 = np.polyfit(Xax, Yax[inds[4]], 1)
#     # fit5_fn = np.poly1d(fit5)
#
#     # axY5.plot( Xax, fit5_fn(Xax), color = 'grey',  linestyle = '--', linewidth = 1.5)
#     # axY4.plot( Xax, fit4_fn(Xax), color = 'grey', linestyle = '--', linewidth = 1.5)
#     # axY3.plot( Xax, fit3_fn(Xax), color = 'grey', linestyle = '--', linewidth = 1.5)
#     # axY2.plot( Xax, fit2_fn(Xax), color = 'grey', linestyle = '--', linewidth = 1.5)
#     # axY1.plot( Xax, fit1_fn(Xax), color = 'grey',linestyle = '--',  linewidth = 1.5)
#
#     axY1.yaxis.set_label_coords(1.05,0.5)
#     axY1.set_ylabel(Ystr[inds[0]])
#     axY2.yaxis.set_label_coords(1.05,0.5)
#     axY2.set_ylabel(Ystr[inds[1]])
#     axY3.yaxis.set_label_coords(1.05,0.5)
#     axY3.set_ylabel(Ystr[inds[2]])
#     axY4.yaxis.set_label_coords(1.05,0.5)
#     axY4.set_ylabel(Ystr[inds[3]])
#     axY5.yaxis.set_label_coords(1.05,0.5)
#     axY5.set_ylabel(Ystr[inds[4]])
# 
#     axY5.xaxis.set_label_coords(1.1,1.15)
#     axY5.set_xlabel('Pressure ')
#
#     # t1 = axY1.text(0.02,0.75, Ystr[inds[0]],  color='black', transform=axY1.transAxes)
#     # t2 = axY2.text(0.02,0.75, Ystr[inds[1]],  color='black', transform=axY2.transAxes)
#     # t3 = axY3.text(0.02,0.75, Ystr[inds[2]],  color='black', transform=axY3.transAxes)
#     # t4 = axY4.text(0.02,0.75, Ystr[inds[3]],  color='black', transform=axY4.transAxes)
#     # t5 = axY5.text(0.02,0.75, Ystr[inds[4]],  color='black', transform=axY5.transAxes)
#
#     plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Reduced2_' + Plotname + '.pdf')
#     plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Reduced2_' + Plotname + '.eps')
#
#
# # plt.show()
