import requests as r 
import configparser
import modin.pandas as pd
import warnings
from datetime import datetime
from domainapi import domain

warnings.filterwarnings("ignore")

#variables
subs_geelong = ['Belmont', 'Grovedale']
subs_melb = ['Yarraville']


#function format(propertyTypes,minBedrooms,minBathrooms,minCarspaces,minPrice,maxPrice,minLandArea,state,region,area,suburb,includeSurroundingSuburbs)
df = domain().listing_results(["House"],3,2,3,1000000,1500000,10,"VIC","","","",False)
#print(df)
print(df.shape)
df1 = df[['id','bedrooms','price','price_min','price_max']]
print(df1.shape)
print(df)



#print(domain().sales_results("Melbourne"))




