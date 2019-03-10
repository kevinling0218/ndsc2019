# Import modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def train_test_data(df, label, test_size):
    '''Prepare training and test data'''
    df = df[['title', label]]
    df = df.dropna()
    X = df['title']
    y = df[label]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size)
    return X_train,X_test,y_train,y_test