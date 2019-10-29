#######################
# Author: Dandan Wang
# NetID: dw862
# Function: clean data, cluster data and predict data.
# ####################

import csv
import pandas as pd
import numpy as np

def extractData():
    myData = pd.read_csv("../collect_and_clean_data/cleaned_residential.csv", sep=',', encoding='latin1')
    myData.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_lb_ghg', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace=True)
    return myData

def insertState(myData):
    df = pd.read_csv("../../population_data/processed_us_zips.csv", sep=',', encoding='latin1')
    df.drop(['Unnamed: 0', 'timezone', 'lat', 'lng', 'city','state_name', 'zcta', 'parent_zcta', 'population', 'density', 'county_fips', 'county_name', 'all_county_weights', 'imprecise', 'military', 'military'], axis = 1, inplace = True)
    myData = pd.merge(myData, df, how = 'left', on = 'zip', right_index = False)
    myData.to_csv("residential.csv")
    return df 

def getCommonAttrs(df0):
    df = pd.read_csv("../collect_and_clean_data/cleaned_commercial.csv", sep=',', encoding='latin1')
    df.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_lb_ghg', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace = True)
    df = pd.merge(df, df0, how = 'left', on = 'zip', right_index = False)
    df.to_csv("common_attrs_commercial.csv")
    df = pd.read_csv("../collect_and_clean_data/cleaned_industrial.csv", sep=',', encoding='latin1')
    df.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_lb_ghg', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace = True)
    df = pd.merge(df, df0, how = 'left', on = 'zip', right_index = False)
    df.to_csv("common_attrs_industrial.csv")

if __name__ == "__main__":
    # Extract useful attributes form the cleaned data.
    myData = extractData()
#    print(myData[:10])
    df = insertState(myData)
    getCommonAttrs(df)
