# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 21:57:10 2019

@author: szabo
"""

import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


df_hh=pd.read_csv('hh_collected_data.csv')

plt.plot(df_hh['T_Room'])
plt.plot(df_hh['T_Set'])
plt.plot(df_hh['T_Set']+0.5)
plt.plot(df_hh['T_Set']-0.5)

T_room=df_hh['T_Room'].values
T_nextPeak_upper=np.zeros(len(T_room), dtype=float)
T_nextPeak_upper.fill(np.nan)
T_nextPeak_lower=np.zeros(len(T_room), dtype=float)
T_nextPeak_lower.fill(np.nan)


ind_peak_upper, _ = find_peaks(T_room, height=0)
#ind_peak_upper=argrelextrema(T_room, np.greater_equal, order=100)
prev_ind=0
for i,ind in enumerate(ind_peak_upper):
    if i==0:
        T_nextPeak_upper[prev_ind:ind]=T_room[ind]
        prev_ind=ind+1
#    elif i==len(ind_peak_upper)-1:
#        T_nextPeak_upper[ind+1:]=np.nan
    else:
        T_nextPeak_upper[prev_ind:ind]=T_room[ind]
        prev_ind=ind+1
    
plt.plot(T_nextPeak_upper)


ind_peak_lower, _ = find_peaks(100-T_room, height=0)
#ind_peak_upper=argrelextrema(T_room, np.greater_equal, order=100)
prev_ind=0
for i,ind in enumerate(ind_peak_lower):
    if i==0:
        T_nextPeak_lower[prev_ind:ind]=T_room[ind]
        prev_ind=ind+1
#    elif i==len(ind_peak_upper)-1:
#        T_nextPeak_upper[ind+1:]=np.nan
    else:
        T_nextPeak_lower[prev_ind:ind]=T_room[ind]
        prev_ind=ind+1
    
plt.plot(T_nextPeak_lower)

plt.show()

ThermoState_Switch=df_hh['Thermostate_Switch'].values

thermo_switch_on=np.append(np.nan,ThermoState_Switch[1:]>ThermoState_Switch[:-1])
thermo_switch_off=np.append(np.nan,ThermoState_Switch[1:]<ThermoState_Switch[:-1])

np.sum(thermo_switch_off[1:])

ind_switch_on=np.where(thermo_switch_on==1)
ind_switch_off=np.where(thermo_switch_off==1)

plt.plot(ind_switch_on[0],T_room[ind_switch_on],'2',markersize=30,color='r')
plt.plot(ind_switch_off[0],T_room[ind_switch_off],'1',markersize=30,color='b')

# create dataframe
dataset=pd.DataFrame({'T_ROOM':T_room,'ThermoState_Switch':ThermoState_Switch,'T_nextPeak_upper':T_nextPeak_upper})




