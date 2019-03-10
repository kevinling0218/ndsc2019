# Import modules
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from NLP.train_test_data import train_test_data

def build_XGB_model():
    """
    Random XGBoost model
    """

    # Build pipeline
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('xgb', XGBClassifier(n_estimators=80, silent=False, n_jobs=-1,
                                               objective='softmax'))])

    # Define parameters for grid search
    parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                  'tfidf__use_idf': (True, False),
                  'xgb__learning_rate': [0.01, 0.1]}

    # Grid search across our parameters, scoring by accuracy
    gs_clf = GridSearchCV(estimator=text_clf, param_grid=parameters, cv=5, iid=False, n_jobs=-1, scoring='accuracy')
    return gs_clf


def train_test_XGB_model(category, column, X_train, y_train):
    XGB_model = build_XGB_model()
    XGB_model.fit(X_train, y_train)
    # Evaluation
    best_params = XGB_model.best_params_
    predicted = XGB_model.predict(X_test)

    # Print the score
    best_params = best_params
    print('Best Parameters: ', best_params)
    train_acc = round(XGB_model.best_score_, 2)
    print('Train Set Accuracy: ', train_acc)
    test_acc = round(np.mean(predicted == y_test), 2)
    print('Test Set Accuracy: ', test_acc)

    with open('XGB_clf_09032019_XGB_{}_{}.pkl'.format(category, column), 'wb') as f:
        pickle.dump(XGB_model, f)

    return XGB_model

beauty_feature_columns = ['Brand', 'Colour_group', 'Benefits']
df_beauty_train = pd.read_csv('../data/beauty_data_info_train_competition.csv')

df_beauty_train = df_beauty_train.head(n=1500)
for column in beauty_feature_columns:
    print ("Now processing for column:", column)
    # Unpack data
    X_train,X_test,y_train,y_test = train_test_data(df_beauty_train, column, 0.1)
    XGB_model = train_test_XGB_model('beauty', column, X_train, y_train)