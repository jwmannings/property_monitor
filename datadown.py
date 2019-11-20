import requests as r 
import configparser
import modin.pandas as pd
from datetime import datetime

#config 
config = configparser.ConfigParser()
config.read('config.ini')

#apis
api_base = "https://api.domain.com.au/v1/"
api_secret = config['domain']['api_secret']
api_salesresults = "salesResults/{city}/listings"
api_listings = "listings/residential/_search"
listings_params: """{{
  "listingType":"Sale",
  "propertyTypes":[
    "House"
    ],
  "minBedrooms":2,
  "minBathrooms":1,
  "minCarspaces":2,
  "minPrice":{min_price},
  "maxPrice":{max_price},
  "minLandArea":500,
  "locations":[
    {
      "state":"VIC",
      "region":"",
      "area":"",
      "suburb":"{suburb}",
      "includeSurroundingSuburbs":false
    }
  ]
}"""
api_propertydetails = "properties/{prop_id}"

#variables
subs_geelong = ['Belmont', 'Grovedale']
subs_melb = ['Yarraville']
version = datetime.now()
version = str(version).replace('-','').replace(' ','')[:10]
