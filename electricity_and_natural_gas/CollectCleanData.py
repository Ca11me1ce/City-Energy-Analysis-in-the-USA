###################
# Author: Dandan Wang
# NetID: dw862
# Function: Collect and clean electricity and natural gas data.
# #################

import requests
import json
import csv
import pandas as pd
from pprint import pprint
from sklearn.datasets.samples_generator import make_moons
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np

def readZipCodes():
    # Read zip codes from processed_us_zips.csv
    myDataFrame = pd.read_csv("../population_data/processed_us_zips.csv", sep=',', encoding='latin1')
    return myDataFrame

def readAPI(API_list):
    # Read APIs in API.txt, and save them into a list.
    with open("API.txt", 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            API_list.append(line)

def defineAttrs():
    with open("residential.csv", 'w') as f1, open("commercial.csv", 'w') as f2, open("industrial.csv", 'w') as f3, open("electricity_and_natural_gas.csv", 'w') as f:
        writer1 = csv.writer(f1, delimiter = ',')
        writer2 = csv.writer(f2, delimiter = ',')
        writer3 = csv.writer(f3, delimiter = ',')
        writer = csv.writer(f, delimiter = ',')
        
        # The residential, commercial and industrial file have some public attributions
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
        # Ignore the maximum and minimum values, and merge other attributes into the electricity_and_natural_gas.csv.
        merged_attrs = ['zip', 
                        'city',
                        'housing_units',
                        'total_pop',
                        'commercial_num_establishments',
                        'industrial_num_establishments',
                        'residential_elec_1kdollars',
                        'commercial_elec_1kdollars',
                        'industrial_elec_1kdollars',
                        'residential_elec_mwh',
                        'commercial_elec_mwh',
                        'industrial_elec_mwh',
                        'residential_gas_1kdollars',
                        'commercial_gas_1kdollars',
                        'industrial_gas_1kdollars',
                        'residential_gas_mcf',
                        'commercial_gas_mcf',
                        'industrial_gas_mcf',
                        'residential_elec_lb_ghg',
                        'commercial_elec_lb_ghg',
                        'industrial_elec_lb_ghg',
                        'residential_gas_lb_ghg',
                        'commercial_gas_lb_ghg',
                        'industrial_gas_lb_ghg']
        writer1.writerow(residential_attrs)
        writer2.writerow(commercial_attrs)
        writer3.writerow(industrial_attrs)
        writer.writerow(merged_attrs)
    return (public_attrs, merged_attrs)

def requestUrl(zipCodes, API_list, public_attrs):
    # Request to get the json-structure content from the website.
    mergedAttrs = ['elec_1kdollars',
                   'elec_mwh',
                   'gas_1kdollars',
                   'gas_mcf',
                   'elec_lb_ghg',
                   'gas_lb_ghg']
    with open("residential.csv", 'a') as f1, open("commercial.csv", 'a') as f2, open("industrial.csv", 'a') as f3, open("electricity_and_natural_gas.csv", 'a') as f:
        writer1 = csv.writer(f1, delimiter = ',')
        writer2 = csv.writer(f2, delimiter = ',')
        writer3 = csv.writer(f3, delimiter = ',')
        writer = csv.writer(f, delimiter = ',')
        length = len(zipCodes)
        start = 0
        # Each API can only get 1000 requests per hour.
        # To request all zip codes whose amount is 32969, there should be 33 different APIs.
        for j in range(len(API_list)):
            if start + 1000 > length:
                # The last API would handle fewer than 1000 requests.
                end = len(zipCodes)
            else:
                end = start + 1000
            # Each API is used to request 1000 zip codes.
            for i in zipCodes['zip'][start: end]:
                # The first 0 is omitted in the processed_us_zip.csv. 
                # The 0 should be added and transfer the numeric variable into string.
                if i < 10000:
                    i = '0' + str(i)
                # When the zip code is 70085, 70091 or 72801, requests will be blocked and failed.
                # Don't request these zip codes.
                if i == 70085 or i == 70091 or i == 72801:
                    continue
                # Send requests to get content.
                query_params = {'zip':i, 'api_key':API_list[j]}
                endpoint = 'https://developer.nrel.gov/api/cleap/v1/energy_expenditures_and_ghg_by_sector?'
                response = requests.get(endpoint, params = query_params)
                txt = json.loads(response.text)
                
                # There are data what we want to collect only when there is no error.
                if txt['errors'] == []: 
                    # The value of key 'result' is the energy data of each city which has the corresponding zip code.
                    result = txt['result']
                    # Each city should be saved as a row.
                    for city in result:
                        # The zip code and city name should be recorded as well.
                        residential_attrs = [i, city]
                        commercial_attrs = [i, city]
                        industrial_attrs = [i, city]
                        merged_attrs = [i, city]
                        
                        # The energy data of each type in the city.
                        residential = result[city]['residential']
                        commercial = result[city]['commercial']
                        industrial = result[city]['industrial']

                        # Collect the private attributes of each type.
                        residential_attrs.append(residential['housing_units'])
                        residential_attrs.append(residential['total_pop'])
                        commercial_attrs.append(commercial['num_establishments'])
                        industrial_attrs.append(industrial['num_establishments'])
                        merged_attrs.append(residential['housing_units'])
                        merged_attrs.append(residential['total_pop'])
                        merged_attrs.append(commercial['num_establishments'])
                        merged_attrs.append(industrial['num_establishments'])

                        # Collect the public attributes.
                        for attr in public_attrs:
                            residential_attrs.append(residential[attr])
                            commercial_attrs.append(commercial[attr])
                            industrial_attrs.append(industrial[attr])
            
                        # Collect the attributes except maximum and minimum attributes.
                        for attr in mergedAttrs:
                            merged_attrs.append(residential[attr])
                            merged_attrs.append(commercial[attr])
                            merged_attrs.append(industrial[attr])
    
                        # Write the energy data of each city as a row.
                        writer1.writerow(residential_attrs)
                        writer2.writerow(commercial_attrs)
                        writer3.writerow(industrial_attrs)
                        writer.writerow(merged_attrs)
                else:
                    # Print out the error code. 
                    # All error codes are "NOT FOUND".
                    print(i, "error code:", txt['errors'])
            # Each API can only request 1000 zip codes because of the rate limitation.
            start = start + 1000

def readData(file_name):
    # READ DATA
    # Read in data directly into pandas
    myData = pd.read_csv(file_name , sep=',', encoding='latin1')
    return myData

def findMissing(myDataFrame):
    # Calculate the fraction of missing values of each column.
    frac = myDataFrame.isna().sum() * 1.00 / len(myDataFrame)
    return frac

def findNoise(myDataFrame):
    # Calculate the fraction of incorrect values of each column.
    frac = []
    for i in myDataFrame:
        frac.append(len(myDataFrame[myDataFrame[i] < 0]) * 1.00 / len(myDataFrame))
    return frac

def pad(myDataFrame, col, attr, i, n):
    # Get the average of i's n neighbors.
    # Use this average to replace the missing value.
    # The half upper neighbors. (Smaller index in the table.)
    upper = n/2
    # The half latter neighbors.
    under = n - n/2
    # S is used to store sum of neighbors.
    s = 0
    # The closest upper neighbor.
    j = i-1
    while j >= 0 and upper > 0:
        if col[j] == False:
            s += myDataFrame[attr][j]
            upper -= 1
        j -= 1    
    # The closest under neighbor.
    j = i+1
    while j < len(myDataFrame) and under > 0:
        if col[j] == False:
            s += myDataFrame[attr][j]
            under -= 1
        j += 1
    # Return the average of neighbors.
    return (s * 1.00) / (n - upper - under)

def cleanData(myDataFrame, attrs, file_name):
    # Clean myDataFrame and save the cleaned data into file_name.
    with open (file_name, 'w') as f:
        # Iterate each column in myDataFrame.
        for attr in attrs:
            # Judge whether an entry in myDataFrame is null or not.
            col = myDataFrame.isna()[attr]
            for e in range(len(col)):
                # When the element (eth element in myDataFrame[attr]) is null.
                if col[e] == True:
                    # Replace the NaN with the average of the null element's neighbors.
                    myDataFrame[attr][e] =  pad(myDataFrame, col, attr, e, 4)
        # Write the cleaned data into the corresponding file.
        myDataFrame.to_csv(f, index=False)

def collectData():
    # Read zip codes from ../population_data/processed_us_zips.csv
    zipCodes = readZipCodes()
    API_list = []
    # Read API from API.txt
    readAPI(API_list)
    # Define the list of residential attributes, commercial attributes, industrial attrs and choose some necessary attributes as the merged data attrs.
    # Write these attributes into related csv files as the name of columns.
    attrs = defineAttrs()
    # Request the contents of URL.
    requestUrl(zipCodes, API_list, attrs[0])
    return attrs

def cleanliness(df_residential, df_commercial, df_industrial, df_merged):
    # Find the number of missing values in each column of each file.
    missing_frac_residential = findMissing(df_residential)
    missing_frac_commercial = findMissing(df_commercial)
    missing_frac_industrial = findMissing(df_industrial)
    missing_frac_merged = findMissing(df_merged)
    print("The fractions of missing values are: \n", "\nresidential:\n", missing_frac_residential, "\n\ncommercial:\n", missing_frac_commercial, "\n\nindustrial:\n", missing_frac_industrial, "\n\nmerged data:\n", missing_frac_merged)
    
    # Find the number of incorrect values in each column of each file.
    incorrect_frac_residential = findNoise(df_residential.drop(['zip', 'city'], axis = 1))
    incorrect_frac_commercial = findNoise(df_commercial.drop(['zip', 'city'], axis = 1))
    incorrect_frac_industrial = findNoise(df_industrial.drop(['zip', 'city'], axis = 1))
    incorrect_frac_merged = findNoise(df_merged.drop(['zip', 'city'], axis = 1))
    print("\nThe fractions of incorrect values are:\n ", "residential:\n", incorrect_frac_residential, "\ncommercial:\n", incorrect_frac_commercial, "\nindustrial:\n", incorrect_frac_industrial, "\nmerged data:\n", incorrect_frac_merged)

if __name__ == "__main__":
    # Collect data.
    attrs = collectData()

    # Read Data into DataFrames
    df_residential = readData("residential.csv")
    df_commercial = readData("commercial.csv")
    df_industrial = readData("industrial.csv")
    df_merged = readData("electricity_and_natural_gas.csv")

    # Detect the cleanliness of data.
    cleanliness(df_residential, df_commercial, df_industrial, df_merged)

    # Clean Data.
    cleanData(df_residential, ['housing_units', 'total_pop'] + public_attrs, "cleaned_residential.csv")
    cleanData(df_commercial, ['num_establishments'] + public_attrs, "cleaned_commercial.csv")
    cleanData(df_industrial, ['num_establishments'] + public_attrs, "cleaned_industrial.csv")
    cleanData(df_merged, merged_attrs, "cleaned_electricity_and_natural_gas.csv")

    # Detect the processed data.
    # Read the processed data into dataframe.
    df_cleaned_residential = readData("cleaned_residential.csv")
    df_cleaned_commercial = readData("cleaned_commercial.csv") 
    df_cleaned_industrial = readData("cleaned_industrial.csv")
    df_cleaned_merged_data = readData("cleaned_electricity_and_natural_gas.csv")
    
    # Detect the cleanliness of processed_data.
    print("\nAfter processed.\n")
    cleanliness(df_cleaned_residential, df_cleaned_commercial, df_cleaned_industrial, df_cleaned_merged_data)
