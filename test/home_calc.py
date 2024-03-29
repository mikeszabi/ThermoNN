# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 09:12:20 2022

@author: szabo
"""
from io import BytesIO

import requests

from matplotlib import pyplot as plt

import pandas as pd
sheet_id = '11WSTbHwSHVpiXz5OQ5GxFfDsV77dJ9pv_AtMTGeS3Jk'
sheet_gid = '1579323792'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={sheet_gid}'

csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')


sp_code='1w'
conv_gas=10 # 1m3 gas heat power in kWh
price_gas=1
price_electric=1


df_scale_data=pd.read_csv(csv_export_url,sep=',',error_bad_lines=False)
cols=df_scale_data.columns

df_scale_data.columns=['Date','Gas','ElectricIn','ElectricOut','Solar','Water','Change','ScaleAtChange']

######################## elektromos fogyasztás

df_scale_electricity=df_scale_data[df_scale_data['ElectricIn'].notnull()].copy()

#date_handling
df_scale_electricity['Date2']=pd.to_datetime(df_scale_electricity['Date'], infer_datetime_format=True)
df_scale_electricity['days']=df_scale_electricity['Date2']-df_scale_electricity['Date2'].shift(1)

df_scale_electricity['hours']=df_scale_electricity['days'].astype('timedelta64[h]')


# consumption
df_scale_electricity['d_electric_in']=df_scale_electricity.loc[:,['ElectricIn']]-df_scale_electricity.loc[:,['ElectricIn']].shift(1)

df_scale_electricity.loc[df_scale_electricity.loc[:,'Change'].shift(1)=='Elektromos mérőóra csere',['d_electric_in']]+=df_scale_electricity.loc[df_scale_electricity.loc[:,'Change']=='Elektromos mérőóra csere',['ScaleAtChange']].values

df_scale_electricity['d_electric_out']=df_scale_electricity.loc[:,['ElectricOut']]-df_scale_electricity.loc[:,['ElectricOut']].shift(1)

df_scale_electricity['d_electric_solar']=df_scale_electricity.loc[:,['Solar']]-df_scale_electricity.loc[:,['Solar']].shift(1)
df_scale_electricity.loc[df_scale_electricity['d_electric_out'].isnull(),['d_electric_out']]=0
df_scale_electricity.loc[df_scale_electricity['d_electric_solar'].isnull(),['d_electric_solar']]=0


df_scale_electricity['d_electric_consumed']=df_scale_electricity['d_electric_in']+df_scale_electricity['d_electric_solar']-df_scale_electricity['d_electric_out']
df_scale_electricity['d_electric_paid']=df_scale_electricity['d_electric_in']-df_scale_electricity['d_electric_out']

df_scale_electricity['d_electric_in_perhour']=df_scale_electricity['d_electric_in']/df_scale_electricity['hours']
df_scale_electricity['d_electric_out_perhour']=df_scale_electricity['d_electric_out']/df_scale_electricity['hours']
df_scale_electricity['d_electric_solar_perhour']=df_scale_electricity['d_electric_solar']/df_scale_electricity['hours']


df_scale_electricity['d_electric_consumed_perhour']=df_scale_electricity['d_electric_consumed']/df_scale_electricity['hours']
df_scale_electricity['d_electric_paid_perhour']=df_scale_electricity['d_electric_paid']/df_scale_electricity['hours']

# reasample and interpolate
df_2plot_electricity=df_scale_electricity.copy()
df_2plot_electricity.index = df_2plot_electricity['Date2']
df_2plot_electricity=df_2plot_electricity.resample(sp_code).pad()

df_2plot_electricity['hours_resample']=(df_2plot_electricity.index.shift(1)-df_2plot_electricity.index).astype('timedelta64[h]')


############################ gáz fogyasztás

df_scale_gas=df_scale_data[df_scale_data['Gas'].notnull()].copy()

#date_handling
df_scale_gas['Date2']=pd.to_datetime(df_scale_gas['Date'], infer_datetime_format=True)
df_scale_gas['days']=df_scale_gas['Date2']-df_scale_gas['Date2'].shift(1)

df_scale_gas['hours']=df_scale_gas['days'].astype('timedelta64[h]')

# consumption
df_scale_gas['d_gas']=df_scale_gas.loc[:,['Gas']]-df_scale_gas.loc[:,['Gas']].shift(1)

df_scale_gas.loc[df_scale_gas.loc[:,'Change'].shift(1)=='Gázmérő csere',['d_gas']]+=df_scale_gas.loc[df_scale_gas.loc[:,'Change']=='Gázmérő csere',['ScaleAtChange']].values

df_scale_gas['d_gas_perhour']=df_scale_gas['d_gas']/df_scale_gas['hours']

# reasample and interpolate
df_2plot_gas=df_scale_gas.copy()
df_2plot_gas.index = df_2plot_gas['Date2']
df_2plot_gas=df_2plot_gas.resample(sp_code).pad()
df_2plot_gas['hours_resample']=(df_2plot_gas.index.shift(1)-df_2plot_gas.index).astype('timedelta64[h]')



# approximate energy plots

fig2, ax2 = plt.subplots()

ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_consumed_perhour'],color='pink',label='Electricity Consumed')
ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_paid_perhour'],color='orange',label='Electricity Paid')

ax2.plot(df_2plot_gas.index,price_gas*conv_gas*df_2plot_gas['hours_resample']*df_2plot_gas['d_gas_perhour'],color='black',label='Gas Consumed')
ax2.plot(df_2plot_gas.index,price_gas*conv_gas*df_2plot_gas['hours_resample']*df_2plot_gas['d_gas_perhour']+df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_consumed_perhour'],color='red',label='Energy Consumed')

ax2.legend(loc='upper left')

# sunpower
fig2, ax2 = plt.subplots()

ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_in_perhour'],color='red',label='From GRID')
ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_out_perhour'],color='green',label='To GRID')
ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*df_2plot_electricity['d_electric_solar_perhour'],color='yellow',label='From PV')
ax2.plot(df_2plot_electricity.index,df_2plot_electricity['hours_resample']*(df_2plot_electricity['d_electric_in_perhour']-df_2plot_electricity['d_electric_out_perhour']),color='blue',label='Paid')


ax2.legend(loc='upper left')
