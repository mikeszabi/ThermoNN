# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:39:49 2019

@author: szabo
"""

df_ts_sel=df_ts[dataset['ThermoState_Switch']==1]
df_ts_sel=df_ts_sel[df_ts_sel['var1(t-10)']<df_ts_sel['var1(t-1)']]

df_ts_sel_norm=df_ts_sel.subtract(df_ts_sel['var1(t-1)'],axis=0)

x=df_ts_sel_norm.values[:,:-1]
x=x.reshape((x.shape[0], x.shape[1],1))

y=df_ts_sel_norm.values[:,-1]


predictions = model.predict_point_by_point(x)

plot_results(predictions, y)
