import requests as r 
import configparser
import modin.pandas as pd
import json
from price_parser import Price
from datetime import datetime
from  jsonmerge import merge


#config 
config = configparser.ConfigParser()
config.read('config.ini')

class domain:
    api_base = "https://api.domain.com.au/v1/"
    api_secret = config['domain']['api_secret']


    '''Docstring -  domain.com.au API access '''

    def _init_(self):
        version = datetime.now()
        self.version = str(version).replace('-','').replace(' ','')[:10]

    def sales_results(self,city):
        '''docstring'''

        acceptable_inputs = ["Sydney", "Melbourne", "Brisbane", "Adelaide", "Canberra"]

        if str(city) in acceptable_inputs:
            pass
        else:
            return("Not an acceptable input")
        api_salesresults = "salesResults/{city_name}/listings".format(city_name=city)

        headers = {'X-API-Key': domain.api_secret}
        url = str(domain.api_base + api_salesresults)
        try:
            listings_call = r.get(url, headers=headers)
        except Exception as e:
            print('Error in API call: ', e)
        
        #sales_results = pd.DataFrame(columns=[[]])

        return listings_call.text


    def listing_results(self, propertyTypes= ["House"],minBedrooms=0,minBathrooms=0,minCarspaces=0,minPrice=0,maxPrice=1000000,minLandArea=0,state="",region="",area="",suburb="",includeSurroundingSuburbs=False):
        '''docstring'''
        api_listings = "listings/residential/_search"
        listings_params = {
        "listingType":"Sale",
        "propertyTypes":propertyTypes,
        "minBedrooms":minBedrooms,
        "minBathrooms":minBathrooms,
        "minCarspaces":minCarspaces,
        "minPrice":minPrice,
        "maxPrice":maxPrice,
        "minLandArea":minLandArea,
        "page:":1,
        "locations":[
            {
            "state":state,
            "region":region,
            "area":area,
            "suburb":suburb,
            "includeSurroundingSuburbs":includeSurroundingSuburbs
            }],
        "pageSize":100
        } 
        
        results = pd.DataFrame(columns=['id','advertiser_type','advertiser_id','price','price_min','price_max','features','property_type','bathrooms','bedrooms','carspaces','region','suburb','postcode','address','latitude','longitude','headline','description','labels','listingSlug'])

        listings_params = json.dumps(listings_params)

        headers = {'X-API-Key': domain.api_secret, 'Content-Type':'application/json'}
        url = str(domain.api_base + api_listings)
        try:
            listings_call = r.post(url, data=listings_params, headers=headers)
        except Exception as e:
            print('Error in API call: ', e)
        if 'errors' in listings_call.json():
            error_log = ('processing error: ',listings_call.json()) 
            
        result_count = listings_call.headers['X-Total-Count']
        pagin_count = listings_call.headers['X-Pagination-PageSize']
        print("results_count: ", result_count)
        print("pagin_count: ", pagin_count)

        if int(result_count) < int(pagin_count):
            print('hit single processing')
            data = listings_call.json()
            for item in data:
                try:
                    #print(item)
                    id = item['listing']['id']
                    advertiser_type = item['listing']['advertiser']['type']
                    advertiser_id = item['listing']['advertiser']['id']
                    price = item['listing']['priceDetails']['displayPrice']
                    if 'auction' in price.lower():
                        price_min = 'AUCTION'
                        price_max = 'AUCTION'
                        price = 'AUCTION'
                    elif 'contact' in price.lower():
                        price_min = 'CONTACT'
                        price_max = 'CONTACT'
                        price = 'CONTACT'
                    elif any(str.isdigit(c) for c in price):
                        price_min_ = Price.fromstring(str(price))
                        price_min = price_min_.amount
                        price_max = price.replace(str(price_min_.amount_text),'')
                        price_max = Price.fromstring(str(price_max))
                        price_max = price_max.amount
                    else:
                        price_min = 'NA'
                        price_max = 'NA'
                        price = 'NA'
                    features = item['listing']['propertyDetails']['features']
                    property_type = item['listing']['propertyDetails']['propertyType']
                    bathrooms = item['listing']['propertyDetails']['bathrooms']
                    bedrooms = item['listing']['propertyDetails']['bedrooms']
                    carspaces = item['listing']['propertyDetails']['carspaces']
                    region = item['listing']['propertyDetails']['region']
                    suburb = item['listing']['propertyDetails']['suburb']
                    postcode = item['listing']['propertyDetails']['postcode']
                    address = item['listing']['propertyDetails']['displayableAddress']
                    latitude = item['listing']['propertyDetails']['latitude']
                    longitude = item['listing']['propertyDetails']['longitude']
                    headline = item['listing']['headline']
                    description = item['listing']['summaryDescription']
                    labels = item['listing']['labels']
                    listingSlug = item['listing']['listingSlug']

                    dict_row = {'id':id, 'advertiser_type':advertiser_type,'advertiser_id':advertiser_id, 'price':price,'price_min':price_min,'price_max':price_max,'features':features,'property_type':property_type,'bathrooms':bathrooms,'bedrooms':bedrooms,'carspaces':carspaces,'region':region,'suburb':suburb,'postcode':postcode,'address':address,'latitude':latitude,'longitude':longitude,'headline':headline,'description':description,'labels':labels,'listingSlug':listingSlug}

                    results = results.append(dict_row, ignore_index=True)
                except Exception as e:
                    print('processing error: ',e) 
            return results
        elif int(result_count) > int(pagin_count):
            print('hit loop processing')
            pages = int(int(result_count)/int(pagin_count))
            for i in range(1,pages):
                page = int(i)
                print("page: ",page)
                globals()['listings_params'+str(i)] = {
                "listingType":"Sale",
                "propertyTypes":propertyTypes,
                "minBedrooms":minBedrooms,
                "minBathrooms":minBathrooms,
                "minCarspaces":minCarspaces,
                "minPrice":minPrice,
                "maxPrice":maxPrice,
                "minLandArea":minLandArea,
                "page":page,
                "locations":[
                    {
                    "state":state,
                    "region":region,
                    "area":area,
                    "suburb":suburb,
                    "includeSurroundingSuburbs":includeSurroundingSuburbs
                    }],
                "pageSize":100
                } 
                
                globals()['listings_params'+str(i)] = json.dumps(globals()['listings_params'+str(i)])
                print(globals()['listings_params'+str(i)])
                headers = {'X-API-Key': domain.api_secret, 'Content-Type':'application/json'}
                url = str(domain.api_base + api_listings)
                try:
                    globals()['listings_call'+str(i)] = r.post(url, data=globals()['listings_params'+str(i)], headers=headers)
                except Exception as e:
                    print('Error in API call in loop: ', e)
                if 'errors' in globals()['listings_call'+str(i)].json():
                    error_log = ('processing error loop: ',globals()['listings_call'+str(i)].json()) 
                print("loop: ",i)
                print("total count: ",globals()['listings_call'+str(i)].headers['X-Total-Count'])
                print("pagination number: ", globals()['listings_call'+str(i)].headers['X-Pagination-PageNumber'])
                globals()['data'+str(i)] = globals()['listings_call'+str(i)].json()
                for item in globals()['data'+str(i)]:
                    try:
                        print('hit processing loop')
                        id = item['listing']['id']
                        advertiser_type = item['listing']['advertiser']['type']
                        advertiser_id = item['listing']['advertiser']['id']
                        price = item['listing']['priceDetails']['displayPrice']
                        if 'auction' in price.lower():
                            price_min = 'AUCTION'
                            price_max = 'AUCTION'
                            price = 'AUCTION'
                        elif 'contact' in price.lower():
                            price_min = 'CONTACT'
                            price_max = 'CONTACT'
                            price = 'CONTACT'
                        elif any(str.isdigit(c) for c in price):
                            price_min_ = Price.fromstring(str(price))
                            price_min = price_min_.amount
                            price_max = price.replace(str(price_min_.amount_text),'')
                            price_max = Price.fromstring(str(price_max))
                            price_max = price_max.amount
                        else:
                            price_min = 'NA'
                            price_max = 'NA'
                            price = 'NA'
                        features = item['listing']['propertyDetails']['features']
                        property_type = item['listing']['propertyDetails']['propertyType']
                        bathrooms = item['listing']['propertyDetails']['bathrooms']
                        bedrooms = item['listing']['propertyDetails']['bedrooms']
                        carspaces = item['listing']['propertyDetails']['carspaces']
                        region = item['listing']['propertyDetails']['region']
                        suburb = item['listing']['propertyDetails']['suburb']
                        postcode = item['listing']['propertyDetails']['postcode']
                        address = item['listing']['propertyDetails']['displayableAddress']
                        latitude = item['listing']['propertyDetails']['latitude']
                        longitude = item['listing']['propertyDetails']['longitude']
                        headline = item['listing']['headline']
                        description = item['listing']['summaryDescription']
                        labels = item['listing']['labels']
                        listingSlug = item['listing']['listingSlug']

                        globals()['dict'+str(i)] = {'id':id, 'advertiser_type':advertiser_type,'advertiser_id':advertiser_id, 'price':price,'price_min':price_min,'price_max':price_max,'features':features,'property_type':property_type,'bathrooms':bathrooms,'bedrooms':bedrooms,'carspaces':carspaces,'region':region,'suburb':suburb,'postcode':postcode,'address':address,'latitude':latitude,'longitude':longitude,'headline':headline,'description':description,'labels':labels,'listingSlug':listingSlug}
                        results = results.append(globals()['dict'+str(i)], ignore_index=True)
                    except Exception as e:
                        print('processing error: ',e) 
            return results

    def listing_single(self, ID):
        '''docstring'''
        api_propertydetails = "properties/{prop_id}".format(prop_id=ID)




