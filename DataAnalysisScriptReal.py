# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:03:52 2021

@author: August
"""
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
#Parameters to be calculated are:
#a. Temperature Difference between thermocouples vs time, (is the temperature fairly uniform or 
#    is there uneven distribution?)
#b. Total energy collected in the water (also average power over that time)
#c. Maximum heating power
file = "RealData.lvm"
    
def readLVMfile(file,skip_header=23):
    return np.genfromtxt(fname=file,skip_header=skip_header)

def extract_column_from_data_with_index(data,column_index):
    return [row[column_index] for row in data]
data = readLVMfile(file)
time = extract_column_from_data_with_index(data,0)
#Temperature = extract_column_from_data_with_index(data,1)
#Temp0 = extract_column_from_data_with_index(data,2)
#Temp1 = extract_column_from_data_with_index(data,3)
 
temp_dataList = []
for i in range(1,7+1):
    temp_dataList.append(extract_column_from_data_with_index(data,i*2-1)) #There's 7 temperature data columns
    #But every second column in the file is temperature, starting with the third



#plt.style.use('seaborn-whitegrid')
#(dataDict[header[0]],dataDict[header[index]])
#fig = plt.figure()
#ax = plt.subplots(1,3)
#print(dataDict[header[2]][0])

def createSubPlot(ax, x_values, y_values, label='', color='b',
                  title=None, xlabel=None, ylabel=None,legend=None,use_offset=False):
    ax.plot(x_values, y_values, color=color, lw=2,label=label)
    ax.set_xlim([min(x_values),max(x_values)])
    ax.grid(color='b',linestyle='-',)
#    if use_offset:
#        ax.ticklabel_format(axis='y',useOffset=False)
    if legend is not None:
        ax.legend(loc="upper left",fontsize="large")
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

#Problem1: temperature from thermocouples as a function of time.
def problem_1(time,temp_data,title):
    fig, ax = plt.subplots()
    createSubPlot(ax,x_values=time,y_values=temp_data,label='Temp1',color='r',title=title,xlabel="time",\
                  ylabel="Temperature $\degree$K")
    plt.show()
problem_1(time,temp_dataList[0],"Temperature by time for 140mm")



def problem_2(time,temp_dataList):
    fig, (ax1,ax2,ax3,ax4,ax5,ax6,ax7) = plt.subplots(7, sharex=True)
    createSubPlot(ax1, time, temp_dataList[0],label="140mm",color='r',title="Temperature\nBy time")
    createSubPlot(ax2, time, temp_dataList[1],label="110mm",color='b',ylabel="Temperature $\degree$K")
    createSubPlot(ax3, time, temp_dataList[2],label="80mm",color='g',\
                  xlabel="Time")
    createSubPlot(ax4, time, temp_dataList[3],label="50mm",color='c')
    createSubPlot(ax5, time, temp_dataList[4],label="ambient",color='m')
    createSubPlot(ax6, time, temp_dataList[5],label="170mm",color='y')
    createSubPlot(ax7, time, temp_dataList[6],label="200mm",color='k')
    fig.subplots_adjust(hspace=0.1, left=0.15)
    ax1.legend(loc="upper right")
    plt.grid(color="grey")
    ax2.legend(loc="upper right")
    plt.grid(color="grey")
    ax3.legend(loc="upper right")
    plt.grid(color="grey")
    ax4.legend(loc="upper right")
    plt.grid(color="grey")
    ax5.legend(loc="upper right",frameon=True)
    #ax5.set_xlim(min(temp_dataList[4])-0.05,max(temp_dataList[4])+0.05)
    plt.grid(color="grey")
    ax6.legend(loc="upper right")
    plt.grid(color="grey")
    ax7.legend(loc="upper right")
    plt.grid(color="grey")
    #plt.legend([ax1,ax2,ax3,ax4,ax5,ax6,ax7],["140mm","110mm","80mm","50mm","ambient","170mm","200mm"])
problem_2(time,temp_dataList)

#we use 25degrees as roomtemperature:
def calc_Q_from_temp_data(temp_data, t0, specific_heat, mass):
    return [(mass * specific_heat * (temperature - t0))/1000 for temperature in temp_data]
#Calculate energy harvested as a function of time.
def problem_3(time,temp_data):
    q = calc_Q_from_temp_data(temp_data,t0=25,specific_heat=4.186,mass=170)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    createSubPlot(ax1,time,temp_data,color='r',title='Test Data',ylabel="temp1 ($\degree$K)")
    createSubPlot(ax2, time, q,ylabel="Q (kJ)",xlabel="time")
    fig.subplots_adjust(hspace=0)
    ax1.set_title("Problem 3")
    plt.show()

#new problem3 solver, by using 5th colum data as t0:
def newcalc_Q_from_temp_data(temp_data, t_amb, specific_heat, mass):
    result = []
    for i in range(len(temp_data)):
        result.append((mass * specific_heat * (temp_data[i] - t_amb[i]))/1000)
    return result

def newproblem_3(time,temp_data,t_amb):
    q = newcalc_Q_from_temp_data(temp_data,t_amb=t_amb,specific_heat=4.186,mass=170)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    createSubPlot(ax1,time,temp_data,color='r',title='Heat energy vs temperature',ylabel="temp1 ($\degree$K)")
    createSubPlot(ax2, time, q,ylabel="Q (kJ)",xlabel="time")
    fig.subplots_adjust(hspace=0)
    ax1.set_title("Temperature & stored heat\n by time (140mm)")
    plt.show()

    
#problem_3(time,temp_dataList[0])
newproblem_3(time,temp_dataList[0],temp_dataList[4])
"""
fig, axs = plt.subplots(3,sharex=True)
fyor index in range(1,len(header)-1):
    axs[index-1].plot(dataDict[header[0]],dataDict[header[index]])
axs[1].set_ylim(1040,1041)
fig.suptitle('plots')
"""




def cleanData1(temp_data,window=201,polyorder=2):
    return savgol_filter(temp_data,window,polyorder)

def cleanData2(dataRow,window=7):
    return pd.Series(dataRow).rolling(window=window).mean()


def heatPower(mass,specific_heat,time,temp_data,plot=False,maxPower=False,interval=1,offset=40):
    Qdiff = []
    for (i) in range(interval,len(temp_data)):
        Qdiff.append(mass*specific_heat *  (sum(temp_data[i-interval:i]) - sum(temp_data[i-interval*2:i-interval])) / \
                    (sum(time[i-interval:i]) - sum(time[i-(interval*2):i-interval])))    
    #Qdiff = np.diff(temp_data)/np.diff(time)*mass * specific_heat
    Qdiff = (Qdiff[offset:])
    Qdiff = ([element/1000 for element in Qdiff])
    if plot:
        fig, ax3 = plt.subplots(1)
        createSubPlot(ax3,time[offset:-interval],Qdiff,ylabel="Qdiff\n(KWatt)")
        ax3.set_title("Heat power\nby time (140mm)")
        ax3.set_ylim(min(Qdiff),max(Qdiff))
        plt.show()
    elif maxPower:
        return max(Qdiff)
    else:
        return Qdiff
 
def heatPowerAvg(mass,specific_heat,time,temp_data,t0):
    Uw = calc_Q_from_temp_data(temp_data,t0=t0,specific_heat=specific_heat,mass=mass)
    return (Uw[-1] - Uw[0]) / ((time[-1] - time[0]))

#print(heatPowerAvg(mass=100,specific_heat=4.186,time=time,temp_data=(cleanData1(temp_dataList[1])),t0=25))


#print("!!!!!!",np.diff(dataDict["Temperature"])/np.sdiff(dataDict["X_Value"]))
##
#heatPower(mass=100,specific_heat=4.186,time=time,temp_data=(temp_dataList[1]),plot=True)

##Clean data:
heatPower(mass=170,specific_heat=4.186,time=time,temp_data=(cleanData1(temp_dataList[0],polyorder=2)),plot=True,interval=1)

#print(heatPower(mass=100,specific_heat=4.186,temp_data=(Temperature),time=time,maxPower=True))
#fig2, axs2 = plt.subplots(3,sharex=True)
#for index in range(1,len(header)-1):
#    axs2[index-1].plot(dataDict[header[0]],dataDict[header[index]])






