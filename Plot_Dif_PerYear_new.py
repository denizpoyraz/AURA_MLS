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
    plt.ylim(250,3)

    ax0.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678

    ax0.errorbar(main_xarray,Yax,xerr=std_main_xarray,label='All',marker="x",color='black',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)

    ax0.legend(loc='upper right',frameon=True,fontsize='small')

    #    #
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/' + plotname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/' + plotname + '.eps')
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

## extra cleaning for frozen solutions


# (df.PreLevel <= 10) &

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


dif_ucint=[]
dif_ucint2=[]
rdif_ucint=[]
rdif2_ucint=[]

mls = []
uccle = []
uccleraw = []

main_dif_ucint=[];
main_dif_ucint2=[];
main_rdif_ucint=[];
main_rdif2_ucint=[]

# always 15,15, first date then pressure index
for dd in range(datesize):

    dif_ucint.append([])
    dif_ucint2.append([])
    rdif_ucint.append([])
    rdif2_ucint.append([])
    # mls.append([])
    # uccle.append([])


    for t in range(presize):

        dif_ucint[dd].append([])
        dif_ucint2[dd].append([])
        rdif_ucint[dd].append([])
        rdif2_ucint[dd].append([])
        main_dif_ucint.append([]);
        main_dif_ucint2.append([]);
        main_rdif_ucint.append([]);
        main_rdif2_ucint.append([])

        mls.append([])
        uccle.append([])
        uccleraw.append([])



mean_ucint=np.zeros((datesize,presize))
mean_ucint2=np.zeros((datesize,presize))

mean_rucint=np.zeros((datesize,presize))
mean_r2ucint=np.zeros((datesize,presize))


main_mean_ucint=np.zeros(presize);
main_mean_ucint2=np.zeros(presize);
main_mean_rucint=np.zeros(presize);
main_mean_r2ucint=np.zeros(presize);

main_median_mls=np.zeros(presize);
main_median_uccle=np.zeros(presize);



main_std_ucint=np.zeros(presize);
main_std_ucint2=np.zeros(presize);
main_std_rucint=np.zeros(presize);
main_std_r2ucint=np.zeros(presize);


std_ucint=np.zeros((datesize,presize))
std_ucint2=np.zeros((datesize,presize))
std_rucint=np.zeros((datesize,presize))
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
            dif_ucint[di][j].append(dfd[di].at[i+j,'Dif_UcIntLin'])
            dif_ucint2[di][j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])

            rdif_ucint[di][j].append(dfd[di].at[i+j,'RDif_UcIntLin'])
            rdif2_ucint[di][j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])


            t = int(i+j)
            # print('i+j', t)
            main_dif_ucint[j].append(dfd[di].at[t,'Dif_UcIntLin'])
            main_dif_ucint2[j].append(dfd[di].at[i+j,'Dif_UcIntLin2'])
            main_rdif_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin'])
            main_rdif2_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin2'])

            mls[j].append(dfd[di].at[i+j,'PO3_MLS'])
            uccle[j].append(dfd[di].at[i+j,'PO3_UcIntLin'])
            uccleraw[j].append(dfd[di].at[i+j,'PO3_UcMedian'])


print('here 0 ', len(main_rdif2_ucint[0]), np.nanmean(main_rdif2_ucint[0]), main_rdif2_ucint[0])
print('here 1', len(main_rdif2_ucint[1]), np.nanmean(main_rdif2_ucint[1]), main_rdif2_ucint[1])

print('end of first filling')
## testing

for ld in range(presize):
    # for the all years



    main_mean_ucint[ld]=np.nanmean(main_dif_ucint[ld])
    main_mean_ucint2[ld]=np.nanmean(main_dif_ucint2[ld])
    main_mean_rucint[ld]=np.nanmean(main_rdif_ucint[ld])
    main_mean_r2ucint[ld]=np.nanmean(main_rdif2_ucint[ld])

    # print(ld, mls[ld])
    # print(ld, uccle[ld])

    main_median_mls[ld]=np.nanmedian(mls[ld])
    main_median_uccle[ld]=np.nanmedian(uccle[ld])

    main_std_ucint[ld]=np.nanstd(main_dif_ucint[ld])
    main_std_ucint2[ld]=np.nanstd(main_dif_ucint2[ld])
    main_std_rucint[ld]=np.nanstd(main_rdif_ucint[ld])
    main_std_r2ucint[ld]=np.nanstd(main_rdif2_ucint[ld])

    # print(ld, ' main_mean_ucint[ld]',  main_mean_ucint2[ld])
    # print(ld, '  main_mean_r2ucint[ld]',   main_mean_r2ucint[ld])


    for l in range(datesize):
        # for the indivudual years
        # mean_ucint2[l,ld] = np.nanmean(dif_ucint2[l][ld])


        mean_rucint[l,ld]=np.nanmean(rdif_ucint[l][ld])


        mean_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanmean(rdif2_ucint[l][ld])


        std_ucint[l,ld]=np.nanstd(dif_ucint[l][ld])


        std_ucint2[l,ld]=np.nanstd(dif_ucint2[l][ld])


        std_rucint[l,ld]=np.nanstd(rdif_ucint[l][ld])


        # std_r2ucint[l,ld] = np.nanstd(rdif2_ucint[l][ld])
        std_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanstd(rdif2_ucint[l][ld])
#

# print(' V2  0th entry, pressure 216' , main_rdif2_ucint[0], 'main_mean_r2ucint ',   main_mean_r2ucint)


print('two')

#
for ik in range(presize):
    # print(ik, mls[ik])
    # print(ik, uccle[ik])
    print(ik, len(mls[ik]), len(uccle[ik]),  )



Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]
#


print('mean_r2ucint 0', mean_r2ucint[0][0])
print('std_r2ucint 0', std_r2ucint[0][0])
print('mean_r2ucint 1', mean_r2ucint[1][0])
print('std_r2ucint 1', std_r2ucint[1][0])
print('main_mean_r2ucint', main_mean_r2ucint[0:2])
print('main_std_r2ucint', main_std_r2ucint[0:2])

print(np.nanmedian(mls[0]), mls[0])
print(np.nanmedian(mls[1]), mls[1])

x =  np.array(mls[0])
x = x[np.logical_not(np.isnan(x))]

data_to_plot = []
pos = [0] * presize

for kk in range(presize):
    y = np.array(main_rdif2_ucint[kk])
    # y = np.array(uccle[kk])

    y = y[np.logical_not(np.isnan(y))]
    main_rdif2_ucint[kk] = y
    data_to_plot.append(y)
    pos[kk] = kk

print(pos)

#
# plotyearly(mean_r2ucint,std_r2ucint,main_mean_r2ucint,main_std_r2ucint,Y,[-60,80],date_label,
#            'MLS-Uccle (%)','P Air (hPa)','RDif2_MLS-Uccle_IntLin_PerYear')
#
fig, ax0 = plt.subplots()
plt.ylim(-100, 700)
# plt.xlim([-60,80])
plt.xlabel('Pressure(hPa)')
plt.ylabel('RDif (%)')
# plt.ylabel('Uccle (mPa)')


ax0.tick_params(axis='both', which='both', direction='in')
ax0.yaxis.set_ticks_position('both')
ax0.xaxis.set_ticks_position('both')
ax0.yaxis.set_minor_locator(AutoMinorLocator(10))
ax0.xaxis.set_minor_locator(AutoMinorLocator(10))
# ax0.set_yscale('log')
# ax0.axhline(y=5, color='red', linestyle='--')

# ax0.axhline(y=0, color='grey', linestyle='--')
# ax0.axhline(y=-5, color='red', linestyle='--')

# ax0.plot(main_median_mls, Y,label='mls', marker="x", color='black',linewidth=2)
# ax0.plot(main_median_uccle, Y,label='uccle', marker="x", color='red',linewidth=2)

# mls = mls[~np.isnan(mls)]


Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]

inty = [int(iy) for iy in Y]
print(inty)

# data_to_plot = [mls[0], mls[1], mls[2], mls[3], mls[4]]
# data_to_plot = [x, main_rdif2_ucint[1], main_rdif2_ucint[2], ]
ax0.boxplot(data_to_plot,  positions=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
# ax0.set_xticks([215, 177, 146, 121, 100, 82, 68, 56, 46, 38, 31, 26, 21, 17, 14, 12, 10, 8, 6, 5])
ax0.set_xticklabels(inty)
ax0.xaxis.set_tick_params(labelsize=8)

# ,   positions=[0,1,2]
ax0.legend(loc='upper right', frameon=True, fontsize='small')

plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/DC' + 'RDif_BoxPlot' + '.pdf')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/DC' + 'RDif_BoxPlot' + '.eps')
plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_2507/DC' + 'RDif_BoxPlot' + '.png')

plt.show()


print(np.median(mls[1]), mls[1])

