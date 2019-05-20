# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 21:57:10 2019

@author: szabo
"""

#https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/

#import sys
#sys.path.append(r'./meter/python/sami')
import os
#os.chdir(r'./prediction')
import json
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def ts_explanatories(df, n_in=1, col=['T_ROOM']):
	n_vars = len(col)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in-1, -1, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	
	return agg


df_hh=pd.read_csv(r'./data/hh_collected_data.csv')
# T_Room_rel is actually T_Heater_rel

fig = plt.figure()
ax = fig.subplots(nrows=2, ncols=1)

ax[0].plot(df_hh['T_Room'])
ax[0].plot(df_hh['T_Set'])
ax[0].plot(df_hh['T_Set']+0.5)
ax[0].plot(df_hh['T_Set']-0.5)

T_set=df_hh['T_Set'].values

T_room=df_hh['T_Room'].values
#T_room=T_room-T_set

ThermoState_Switch=df_hh['Thermostate_Switch'].values

T_nextPeak_upper=np.zeros(len(T_room), dtype=float)
T_nextPeak_upper.fill(np.nan)
T_nextPeak_lower=np.zeros(len(T_room), dtype=float)
T_nextPeak_lower.fill(np.nan)


ind_peak_upper, _ = find_peaks(T_room, height=0)

mean_cycle_length=np.mean(ind_peak_upper[1:]-ind_peak_upper[:-1])/60 # in minutes

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
    
ax[0].plot(T_nextPeak_upper)


ind_peak_lower, _ = find_peaks(100-T_room, height=0)

mean_cycle_length=np.mean(ind_peak_lower[1:]-ind_peak_lower[:-1]) # in minutes

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
    
ax[0].plot(T_nextPeak_lower)


thermo_switch_on=np.append(np.nan,ThermoState_Switch[1:]>ThermoState_Switch[:-1])==1
thermo_switch_off=np.append(np.nan,ThermoState_Switch[1:]<ThermoState_Switch[:-1])==1

np.sum(thermo_switch_off[1:])

ind_switch_on=np.where(thermo_switch_on==1)
ind_switch_off=np.where(thermo_switch_off==1)

ax[0].plot(ind_switch_on[0],T_room[ind_switch_on],'2',markersize=30,color='r')
ax[0].plot(ind_switch_off[0],T_room[ind_switch_off],'1',markersize=30,color='b')

# new dataset
dataset=pd.DataFrame({'T_ROOM':T_room,'T_Set':T_set,'ThermoState_Switch':ThermoState_Switch,'Thermo_Switch_On':thermo_switch_on,'Thermo_Switch_Off':thermo_switch_off,'T_nextPeak_upper':T_nextPeak_upper})


# create processed dataframe for prediction
configs = json.load(open('config.json', 'r'))

#
cols=configs['data']['columns']
seq_len=configs['data']['sequence_length']

df_ts=ts_explanatories(dataset['T_ROOM'], n_in=seq_len, col=['T_ROOM'])
# set predicted
#df_ts.rename(columns={'var1(t)':'y'})
df_ts['y']=dataset['T_nextPeak_upper']

df_ts_norm=df_ts.subtract(df_ts['var1(t-0)'],axis=0)


# select
df_ts_sel_norm=df_ts_norm[dataset['Thermo_Switch_Off']]


df_ts_sel_norm.to_csv(r'./data/hh_processed_data.csv',float_format='%.3f')




