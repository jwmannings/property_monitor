import requests as r 
import configparser
import modin.pandas as pd
import warnings
import numpy as np
from ast import literal_eval
from datetime import datetime
from domainapi import domain
from functions import processing

warnings.filterwarnings("ignore")


version = datetime.now()
version = str(version).replace('-','').replace(' ','')[:10]

#variables
subs_geelong = ['Belmont', 'Grovedale']
subs_melb = ['Yarraville']
get_data = False
compute_features = False
static_pkl = 'data/2019120723_data.pkl'
feature_ranking = pd.read_csv('input/feature_ranking.csv')

if get_data:
    #function format(propertyTypes,minBedrooms,minBathrooms,minCarspaces,minPrice,maxPrice,minLandArea,state,region,area,suburb,includeSurroundingSuburbs)
    #dont use zeros here yet needs to be fixed
    df = domain().listing_results(["House"],2,1,1,500000,550000,10,"VIC","","","",False)

    print("Main frame shape: ",df.shape)

    df.to_csv('data/{version}_data.csv'.format(version=version), sep='\t', encoding='utf-8')
    df.to_pickle('data/{version}_data.pkl'.format(version=version))
    #dup_df_2 = df[df['id'].duplicated() == True]
    #dup_df_2 = dup_df_2.sort_values(by=['id'])
    #r, c = dup_df_2.shape
    #if r > 0:
    #    print("duplicates in df")
else:
    df = pd.read_pickle(static_pkl)

if compute_features:
    features = processing.compute_features(df)
    print(features)
    '''['BuiltInWardrobes', 'SecureParking', 'AirConditioning', 'Ensuite', 'Gas', 'Heating', 'Dishwasher', 'BalconyDeck', 'InternalLaundry', 'PetsAllowed', 'Bath', 
    'Study', 'FullyFenced', 'Floorboards', 'BroadbandInternetAccess', 'GardenCourtyard', 'AlarmSystem', 'Shed', 'Gym', 'Intercom', 'SolarPanels', 'WaterViews', 
    'Furnished', 'NorthFacing', 'SwimmingPool', 'RainwaterStorageTank', 'CableOrSatellite', 'GroundFloor', 'SolarHotWater', 'TennisCourt', 'OutdoorSpa', 
    'DoubleGlazedWindows', 'WallCeilingInsulation', 'SeparateDiningRoom', 'IndoorSpa']'''
else:
    pass

df = processing.feature_score(df,feature_ranking)
print(df)
df.to_csv('data/{version}_data_featurescored.csv'.format(version=version), sep='\t', encoding='utf-8')