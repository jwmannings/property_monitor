import requests as r 
import configparser
import modin.pandas as pd
import warnings
import numpy as np
from ast import literal_eval
from datetime import datetime
from domainapi import domain

warnings.filterwarnings("ignore")

class processing:

    def _init_(self, pls):
        '''docstring'''
        self.pls = pls

    def feature_score(df, feature_df):
        '''docstring'''
        df['feature_score'] = np.nan

        for index, row in df.iterrows():
            score_list = []
            #print(row['features'])
            for i in row['features']:
                #print(i)
                score = feature_df.loc[feature_df['ref'] == i]['rank']
                #print(score)
                score_list.append(score)
            total_score = sum(int(i) for i in score_list)
            #print('Sum: ',total_score)
            df.loc[df.index[index], 'feature_score'] = total_score
        return df

    def compute_features(df):
        '''docstring'''
        #get unique values from features 
        features_df = df['features']
        features_df = features_df.to_frame()

        features_list = []

        for index, row in features_df.iterrows():
            features_list.append(row['features'])

        flat_list = []
        flat_list = [item for sublist in features_list for item in sublist]

        unique_list = []
        for item in flat_list:
            if item not in unique_list:
                unique_list.append(item)
            else:
                pass

        return unique_list