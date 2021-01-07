# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 21:12:34 2021

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

hist_interval=0.5
sampling_freq=1/10 # seconds
heating_capacity=5000 #watt
heated_area=350 #m3 air
heating_capacity=heated_area*40/1000 #kW
heating_efficiency=0.6 #0.6 gas, 1 electricity
heating_price=12 # gas, 36 electricity HUF/kW

data_folder=r'e:\GoogleDrive\DigDeepHub\Projects\OptiTherm\Data'
data_id='Simulation'
data_file='hh_collected_data_dummy_20190504.csv'
data_folder=os.path.join(data_folder,data_id)
data_file=os.path.join(data_folder,data_file)

df_hh=pd.read_csv(data_file)


T_set=df_hh['T_Set'].values

T_room=df_hh['T_Room'].values

ThermoState_Switch=df_hh['Thermostate_Switch'].values


thermo_switch_on=np.append(np.nan,ThermoState_Switch[1:]>ThermoState_Switch[:-1])==1
thermo_switch_off=np.append(np.nan,ThermoState_Switch[1:]<ThermoState_Switch[:-1])==1

# np.sum(thermo_switch_off[1:])

ind_switch_on=np.where(thermo_switch_on==1)[0]
ind_switch_off=np.where(thermo_switch_off==1)[0]
if ind_switch_on[0]>ind_switch_off[0]:
    ind_switch_off=ind_switch_off[1:]
ind_switch_on=ind_switch_on[0:len(ind_switch_off)]

# plot

fig = plt.figure()
ax = fig.subplots(nrows=1, ncols=1)

ax.plot(df_hh['T_Room'])
ax.plot(df_hh['T_Set'])
ax.plot(df_hh['T_Set']+hist_interval)
ax.plot(df_hh['T_Set']-hist_interval)

ax.plot(ind_switch_on,T_room[ind_switch_on],'2',markersize=30,color='r')
ax.plot(ind_switch_off,T_room[ind_switch_off],'1',markersize=30,color='b')

# new dataset
dataset=pd.DataFrame({'T_ROOM':T_room,'T_Set':T_set,'ThermoState_Switch':ThermoState_Switch,
                      'Thermo_Switch_On':thermo_switch_on,'Thermo_Switch_Off':thermo_switch_off})


### statistics
hh_statistics={}

hh_statistics['test_days']=len(ThermoState_Switch)*10/60/60/24

# átlagos ciklusidők hőmérsékleti csúcsértékek között
ind_peak_upper, _ = find_peaks(T_room, height=0)
temp_cycles=ind_peak_upper[1:]-ind_peak_upper[:-1]

hh_statistics['mean_tempcyle_secs']=np.mean(temp_cycles)/sampling_freq # in seconds
hh_statistics['min_tempcyle_secs']=np.min(temp_cycles)/sampling_freq # in seconds
hh_statistics['max_tempcyle_secs']=np.max(temp_cycles)/sampling_freq # in seconds

# ind_peak_lower, _ = find_peaks(100-T_room, height=0)

# mean_cycle_length_low=np.mean(ind_peak_lower[1:]-ind_peak_lower[:-1])/sampling_freq # in seconds

# 
# fűtéssel töltött idő aránya
heating_periods=ind_switch_off[:-1]-ind_switch_on[:-1]
heating_cycle=ind_switch_on[1:]-ind_switch_on[:-1]
heating_pct=heating_periods/heating_cycle

hh_statistics['mean_heatcyle_secs']=np.mean(heating_cycle)/sampling_freq # in seconds
hh_statistics['min_heatcyle_secs']=np.min(heating_cycle)/sampling_freq # in seconds
hh_statistics['max_heatcyle_secs']=np.max(heating_cycle)/sampling_freq # in seconds

hh_statistics['mean_heatinterval_secs']=np.mean(heating_periods)/sampling_freq # in seconds
hh_statistics['min_heatinterval_secs']=np.min(heating_periods)/sampling_freq # in seconds
hh_statistics['max_heatinterval_secs']=np.max(heating_periods)/sampling_freq # in seconds

hh_statistics['mean_heatpct']=np.mean(heating_pct)
hh_statistics['min_heatpct']=np.min(heating_pct)
hh_statistics['max_heatpct']=np.max(heating_pct)


########

fig = plt.figure()
ax = fig.subplots(nrows=2, ncols=2)

hist,bin_edges=np.histogram(temp_cycles)
ax[0,0].hist(temp_cycles,bins=bin_edges, color='#0504aa',alpha=0.7)
ax[0,0].grid(axis='y', alpha=0.75)
ax[0,0].set_xlabel('seconds (sec)')
ax[0,0].set_ylabel('frequency')
ax[0,0].set_title('Temperature cycle', fontsize=16)

hist,bin_edges=np.histogram(heating_periods)
ax[0,1].hist(heating_periods,bins=bin_edges, color='#0504aa',alpha=0.7)
ax[0,1].grid(axis='y', alpha=0.75)
ax[0,1].set_xlabel('seconds (sec)')
ax[0,1].set_ylabel('frequency')
ax[0,1].set_title('Heating periods', fontsize=16)

hist,bin_edges=np.histogram(heating_cycle)
ax[1,0].hist(heating_cycle,bins=bin_edges, color='#0504aa',alpha=0.7)
ax[1,0].grid(axis='y', alpha=0.75)
ax[1,0].set_xlabel('seconds (sec)')
ax[1,0].set_ylabel('frequency')   
ax[1,0].set_title('Heating cycle', fontsize=16)

hist,bin_edges=np.histogram(heating_pct)
ax[1,1].hist(heating_pct,bins=bin_edges, color='#0504aa',alpha=0.7)
ax[1,1].grid(axis='y', alpha=0.75)
ax[1,1].set_xlabel('pct')
ax[1,1].set_ylabel('frequency')
ax[1,1].set_title('Heating period pct', fontsize=16)

### energy consumption

cur_heat=ThermoState_Switch*heating_capacity*heating_efficiency
cum_heat=np.cumsum(cur_heat)/sampling_freq/60/60
daily_cumconsumption=cum_heat[::int(60*60*24*sampling_freq)]
daily_consumption=daily_cumconsumption[1:]-daily_cumconsumption[:-1]

fig = plt.figure()
ax = fig.subplots(nrows=2, ncols=1)
ax[0].plot(daily_consumption)
ax[0].set_xlabel('days')
ax[0].set_ylabel('consumption - kWh')   
ax[0].set_title('Heating consumption per day', fontsize=16)

ax[1].plot(daily_cumconsumption)
ax[1].set_xlabel('days')
ax[1].set_ylabel('consumption - kWh')   
ax[1].set_title('Accumulated heating consumption', fontsize=16)

