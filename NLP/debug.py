# Import modules
import pandas as pd
import numpy as np
import pickle
import json
# Import sklearn modules
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import SGDClassifier
from NLP.util import category_json, category_feature_columns
from NLP.util import train_test_data
from NLP.util import column_class_to_text, column_text_to_class

# Pandas printing setting
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth', 0)

def array_to_class_list(model, result_array):
    """Return a tuple of class_1,class_2"""
    class_string_1 = str(int(model.classes_[result_array[0]]))
    class_string_2 = str(int(model.classes_[result_array[1]]))
    return class_string_1,class_string_2

def array_to_class_string(model, result_array):
    """This function takes output from load_and_predict and find out the class from SGD.classes_ method
    joint with space to fulfill the competition format"""
    class_string_1 = str(int(model.classes_[result_array[0]]))
    class_string_2 = str(int(model.classes_[result_array[1]]))
    result_string = ''
    result_string = result_string + class_string_1 + " " + class_string_2
    return result_string


def load_and_predict_debug(cat, df, n, column, X_test):
    """This is to load the pkl module and output the 2 classes
    This function is used for debug mode
    """
    # Load the model
    with open('./NLP/SGD_clf_21032019_{0}_{1}.pkl'.format(cat, column), 'rb') as f:
        SGD_clf = pickle.load(f)

    # Predict the probability for 2 classes
    result_prob = SGD_clf.predict_proba(X_test)
    result_prob_2_array = np.array([best_n_prob(2, i) for i in result_prob])
    result_class = np.array([best_n_classes(2, i) for i in result_prob])
    result_class_2_array = [array_to_class_list(SGD_clf, i) for i in result_class]

    class_1 = np.array([item[0] for item in result_class_2_array])
    class_2 = np.array([item[1] for item in result_class_2_array])

    prob_1 = np.array([item[0] for item in result_prob_2_array])
    prob_2 = np.array([item[1] for item in result_prob_2_array])

    print(class_1, class_2, prob_1, prob_2)
    df[column + '_predicted_1'] = pd.Series(class_1)
    df[column + '_predicted_1_prob'] = pd.Series(prob_1)
    df[column + '_predicted_2'] = pd.Series(class_2)
    df[column + '_predicted_2_prob'] = pd.Series(prob_2)
    #     for index, row in df_beauty_val.iterrows():
    #         row[column] = array_to_class_string(row[column])

    return df

def best_n_classes(n, full_array):
    return np.flip(np.argpartition(full_array, -n)[-n:])

def best_n_prob(n, full_array):
    return np.flip(full_array[np.argpartition(full_array, -n)[-n:]])

def check_column_debug(df, column):
    df_check_result = df[['title', column, column+'_predicted_1', column+'_predicted_1_prob', column+'_predicted_2', column+'_predicted_2_prob']]
    df_check_result.dropna(subset = [column], inplace = True)
    df_check_result = df_check_result.loc[~(df_check_result[column] == df_check_result[column+'_predicted_1'])]
    return df_check_result


df_beauty_debug = pd.read_csv('./data/beauty_data_info_train_competition.csv')
df_fashion_debug = pd.read_csv('./data/fashion_data_info_train_competition_new.csv')
df_mobile_debug = pd.read_csv('./data/mobile_data_info_train_competition.csv')


def debug_fashion():
    df_fashion_compare = df_fashion_debug.sample(frac=0.1).head(n=1)

    X_compare_test = df_fashion_compare['title']
    for column in category_feature_columns['fashion']:
        print("Now comparing for column:", column)
        df_fashion_compare = load_and_predict_debug('fashion', df_fashion_compare, 2, column, X_compare_test)
    return df_fashion_compare

df_fashion_compare = debug_fashion()