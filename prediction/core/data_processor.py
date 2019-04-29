import numpy as np
import pandas as pd




class DataLoader():
    """A class for loading and transforming data for the lstm model"""

    def __init__(self, filename, split):
        self.df = pd.read_csv(filename)
        # remove index col
        self.df.drop(self.df.columns[0], axis=1, inplace=True)
        self.shuffle_and_split(split)
        
        
    def shuffle_and_split(self,split):   
        
        self.data_train=self.df.sample(frac=split,random_state=200)
        self.data_test=self.df.drop(self.data_train.index)
        
        self.len_train  = len(self.data_train)
        self.len_test   = len(self.data_test)

    def get_train_data(self):
        x=self.data_train.values[:,:-1]
        y=self.data_train.values[:,-1]
        x=x.reshape((x.shape[0], x.shape[1],1))
        return x,y
    
    def get_test_data(self):
        x=self.data_test.values[:,:-1]
        y=self.data_test.values[:,-1]
        x=x.reshape((x.shape[0], x.shape[1],1))
        return x,y

#    def generate_train_batch(self, batch_size):
#        '''Yield a generator of training data from filename on given list of cols split for train/test'''
#        i = 0
#        while i < (self.len_train):
#            x_batch = []
#            y_batch = []
#            for b in range(batch_size):
#                xy=self.data_train.iloc[i].values
#                x_batch.append(xy[:-1])
#                y_batch.append(xy[-1])
#                i += 1
#            yield np.array(x_batch), np.array(y_batch)
#
#
#    def generate_test_batch(self, batch_size):
#        '''Yield a generator of test data from filename on given list of cols split for train/test'''
#        i = 0
#        while i < (self.len_test):
#            x_batch = []
#            y_batch = []
#            for b in range(batch_size):
#                xy=self.data_test.iloc[i].values
#                x_batch.append(xy[:-1])
#                y_batch.append(xy[-1])
#                i += 1
#            yield np.array(x_batch), np.array(y_batch)
    