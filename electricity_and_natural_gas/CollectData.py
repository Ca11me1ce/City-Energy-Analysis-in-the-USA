###################
# Author: Dandan Wang
# NetID: dw862
# Function: Collect Electricity and Natural Gas Data.
# #################

import requests
import json
import csv
import pandas as pd
from pprint import pprint

def readZipCodes():
    myDataFrame = pd.read_csv("../population_data/processed_us_zips.csv", sep=',', encoding='latin1')
    return myDataFrame

def readAPI(API_list):
    with open("API.txt", 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            API_list.append(line)

def defineAttrs():
    with open("residential.csv", 'w') as f1, open("commercial.csv", 'w') as f2, open("industrial.csv", 'w') as f3:
        writer1 = csv.writer(f1, delimiter = ',')
        writer2 = csv.writer(f2, delimiter = ',')
        writer3 = csv.writer(f3, delimiter = ',')
        # Three files have some public attributions
        public_attrs = ['elec_1kdollars',
                        'elec_mwh',
                        'gas_1kdollars',
                        'gas_mcf',
                        'elec_1kdollars_bin_min',
                        'elec_1kdollars_bin_max',
                        'elec_mwh_bin_min',
                        'elec_mwh_bin_max',
                        'gas_1kdollars_bin_min',
                        'gas_1kdollars_bin_max',
                        'gas_mcf_bin_min',
                        'gas_mcf_bin_max',
                        'elec_lb_ghg',
                        'elec_min_lb_ghg',
                        'elec_max_lb_ghg',
                        'gas_lb_ghg',
                        'gas_min_lb_ghg',
                        'gas_max_lb_ghg']
        residential_attrs = ['zip', 'city', 'housing_units', 'total_pop'] + public_attrs
        commercial_attrs = ['zip', 'city', 'num_establishments'] + public_attrs
        industrial_attrs = ['zip', 'city', 'num_establishments'] + public_attrs
        writer1.writerow(residential_attrs)
        writer2.writerow(commercial_attrs)
        writer3.writerow(industrial_attrs)
    return public_attrs

def requestUrl(zipCodes, API_list, public_attrs):
    with open("residential.csv", 'a') as f1, open("commercial.csv", 'a') as f2, open("industrial.csv", 'a') as f3:
        writer1 = csv.writer(f1, delimiter = ',')
        writer2 = csv.writer(f2, delimiter = ',')
        writer3 = csv.writer(f3, delimiter = ',')
        length = len(zipCodes)
        start = 0
        # Each API can only get 1000 requests per hour.
        # To request all zip codes whose amount is 32969, there should be 33 APIs.
        for j in range(len(API_list)):
            if start + 1000 > length:
                end = len(zipCodes)
            else:
                end = start + 1000
            # Each API is used to request 1000 zip codes.
            for i in zipCodes['zip'][start: end]:
                if i < 10000:
                    i = '0' + str(i)
                query_params = {'zip':i, 'api_key':API_list[j]}
                endpoint = 'https://developer.nrel.gov/api/cleap/v1/energy_expenditures_and_ghg_by_sector?'
                response = requests.get(endpoint, params = query_params)
                txt = json.loads(response.text)
                if txt['errors'] == []: 
                    result = txt['result']
                    for city in result:
                        residential_attrs = [i, city]
                        commercial_attrs = [i, city]
                        industrial_attrs = [i, city]
                        residential = result[city]['residential']
                        commercial = result[city]['commercial']
                        industrial = result[city]['industrial']
                        residential_attrs.append(residential['housing_units'])
                        residential_attrs.append(residential['total_pop'])
                        commercial_attrs.append(commercial['num_establishments'])
                        industrial_attrs.append(industrial['num_establishments'])
                        for attr in public_attrs:
                            residential_attrs.append(residential[attr])
                            commercial_attrs.append(commercial[attr])
                            industrial_attrs.append(industrial[attr])
                        writer1.writerow(residential_attrs)
                        writer2.writerow(commercial_attrs)
                        writer3.writerow(industrial_attrs)
                else:
                    print(i, "error code:", txt['errors'])
            start = start + 1000

if __name__ == "__main__":
    # Read zip codes from ../population_data/processed_us_zips.csv
    zipCodes = readZipCodes()
    API_list = []
    # Read API from API.txt
    readAPI(API_list)
    public_attrs = []
    # Define the list of residential attributes, commercial attributes and industrial attrs.
    # Write these attributes into related csv files as the name of columns.
    public_attrs = defineAttrs()
    # Request the contents of URL.
    requestUrl(zipCodes, API_list, public_attrs)
    
