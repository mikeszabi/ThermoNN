# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:39:49 2019

@author: szabo
"""

#df_ts_sel_norm=df_ts_norm[dataset['ThermoState_Switch']==1]
#df_ts_sel_norm=df_ts_sel_norm[df_ts_sel_norm['var1(t-9)']<df_ts_sel_norm['var1(t-0)']]
#

x=df_ts_norm.values[:,:-1]
x=x.reshape((x.shape[0], x.shape[1],1))

x=x.squeeze()
y=df_ts_norm.values[:,-1]


predictions = model.predict_point_by_point(x)


y=y+dataset['T_ROOM']
predictions=predictions+dataset['T_ROOM']



fig = plt.figure(facecolor='white')
ax = fig.add_subplot(111)
ax.plot(y, label='True Data')
plt.plot(predictions, label='Prediction')
plt.legend()
plt.show()

ax.plot(ind_switch_on[0],T_room[ind_switch_on],'2',markersize=30,color='r')
ax.plot(ind_switch_off[0],T_room[ind_switch_off],'1',markersize=30,color='b')
ax.plot(T_set,color='g')


