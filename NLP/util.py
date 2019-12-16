### This records all the utility functions that we are using

# Import modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from NLP.features import category_json, category_feature_columns

def train_test_data(df, label, test_size):
    '''Prepare training and test data'''
    df = df[['title', label]]
    df = df.dropna()
    X = df['title']
    y = df[label]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size)
    return X_train,X_test,y_train,y_test


def df_class_to_text(df, category):
    """This function convert the entire numeric dataframe into text dataframe"""

    map_json = category_json[category]
    column_map = {}
    for column in category_feature_columns[category]:
        column_map[column] = {v: k for k, v in map_json[column].items()}
        df.loc[:, column] = df[column].map(column_map[column])

    return df

def column_class_to_text(df, category, column):
    """This function is to convert the dataframe with only one single feature column into text
    This is used in the debugging mode
    """
    map_json = category_json[category]
    column_map = {}
    column_map[column] = {v: k for k, v in map_json[column].items()}
    df.loc[:, column] = df[column].map(column_map[column])
    df.loc[:, column+'_predicted'] = df[column+'_predicted'].map(column_map[column])
    return df

def column_class_to_text_debug(df, category, column):
    """This function is to convert the dataframe with only one single feature column into text
    This is used in the debugging mode
    """
    map_json = category_json[category]
    column_map = {}
    column_map[column] = {v: k for k, v in map_json[column].items()}
    df.loc[:, column] = df[column].map(column_map[column])
    df.loc[:, column+'_predicted_1'] = df[column+'_predicted_1'].map(column_map[column])
    df.loc[:, column + '_predicted_2'] = df[column + '_predicted_2'].map(column_map[column])
    return df

def column_text_to_class_debug(df, category, column):
    map_json = category_json[category]
    column_map = {}
    column_map[column] = {k: v for k, v in map_json[column].items()}
    df.loc[:, column] = df[column].map(column_map[column])
    # df.loc[:, column + '_predicted'] = df[column + '_predicted'].map(column_map[column])
    return df

def column_text_to_class(df, category):
    map_json = category_json[category]
    column_map = {}
    for column in category_feature_columns[category]:
        column_map[column] = {k: v for k, v in map_json[column].items()}
    df.loc[:, column] = df[column].map(column_map[column])
    # df.loc[:, column + '_predicted'] = df[column + '_predicted'].map(column_map[column])
    return df