# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 12:29:52 2019

@author: pointcloud
"""

#https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import pandas as pd

def create_dataset(dataset, look_back=1,i_x=0,i_y=2):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), i_x]
		dataX.append(a)
		dataY.append(dataset[i + look_back, i_y])
	return np.array(dataX), np.array(dataY)
# fix random seed for reproducibility
np.random.seed(7)
# load the dataset

values = dataset.values
# integer encode direction
#encoder = LabelEncoder()
#values[:,4] = encoder.fit_transform(values[:,4])
values=values.astype('float32')
# normalize the dataset
#scaler = MinMaxScaler(feature_range=(0, 1))
#values = scaler.fit_transform(values)
# split into train and test sets
train_size = int(len(values) * 0.67)
test_size = len(values) - train_size
train, test = values[0:train_size,:], values[train_size:len(values),:]
# reshape into X=t and Y=t+1
look_back = 3
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
# create and fit the LSTM network
batch_size = 1
model = Sequential()
model.add(LSTM(50, batch_input_shape=(batch_size, trainX.shape[1], trainX.shape[2]), stateful=True))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
for i in range(10):
	model.fit(trainX, trainY, epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
	model.reset_states()
# make predictions
trainPredict = model.predict(trainX, batch_size=batch_size)
model.reset_states()
yhat = model.predict(testX, batch_size=batch_size)

# calculate RMSE
rmse = np.sqrt(mean_squared_error(yhat, testY))
print('Test RMSE: %.3f' % rmse)


plt.plot(yhat)
plt.plot(testY)
plt.show()