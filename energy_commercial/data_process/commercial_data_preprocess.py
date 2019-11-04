import sys
import numpy as np
import pandas as pd
from pprint import pprint

def main(argv):
    # read the dataset from clean_commercial_building.csv and calculate the items number
    dataFrame = pd.read_csv('cleaned_commercial_building.csv', sep=',', encoding='latin1')
    print(dataFrame.shape[0])
    # drop the duplicated lines and calculate the items
    dataFrame = handleDuplicate(dataFrame)
    print(dataFrame.shape[0])
    # calculate the weight of every industry and generate business.csv
    handleTotalBusiness(dataFrame)

    # drop the useless columns
    df_business = pd.read_csv('business.csv', sep=',', encoding='latin1')
    deleteColumn(dataFrame)
    # obtain each city's electricity and gas weight(score)
    df_clean = pd.read_csv('cleaned_attribute.csv', sep=',', encoding='latin1')
    calBusinessScore(df_clean, df_business)

    # merge two dataframe based on city and state_abbr
    df_business_scores = pd.read_csv('business_score.csv', sep=',', encoding='latin1')
    df_other = pd.read_csv('common_attrs_commercial.csv', sep=',', encoding='latin1')
    merge(df_business_scores, df_other)

def handleDuplicate(dataFrame):
    # drop the attribute index and zip
    x = [0, 3]
    dataFrame.drop(dataFrame.columns[x], axis=1, inplace=True)
    dataFrame = dataFrame.drop_duplicates()

    return dataFrame

def handleTotalBusiness(dataFrame):
    # group the dataframe based on the electricity_users which represents industry and the total building number of each industry
    group = dataFrame.groupby(by=['electricity_users'], as_index=False)
    se_group = group.size()
    dict_group = {'electricity_users': se_group.index, 'building_num': se_group.values}
    df_group = pd.DataFrame(dict_group)

    # calculate the total electricity/gas usage of each industry and combine the dataframe
    business1 = group['electricity_use_per_establishment'].sum()
    business2 = group['natural_gas_use_per_establishment'].sum()
    business3 = pd.merge(business1, business2)
    business = pd.merge(business3, df_group)
    business.rename(columns={'electricity_users':'business'}, inplace=True)

    # calculate the mean electricity/gas usage per establishment in each industry
    business['mean_elec'] = business['electricity_use_per_establishment'] / business['building_num']
    business['mean_gas'] = business['natural_gas_use_per_establishment'] / business['building_num']

    business.to_csv('business.csv', index = False)

def deleteColumn(dataFrame):
    x = [0, 2, 4, 7, 8, 9, 10, 11, 13, 14, 15, 16]
    dataFrame.drop(dataFrame.columns[x], axis=1, inplace=True)
    dataFrame.rename(columns={'town':'city'}, inplace=True)
    dataFrame.to_csv('cleaned_attribute.csv', index=False)

def calBusinessScore(df_clean, df_business):
    # group the dataframe based on city,state_abbr, and electricity_users 
    # and calculate the total number of establishment of electricity or gas in each group
    group = df_clean.groupby(by=['city','state_abbr','electricity_users'], as_index=False)
    number_of_electricity_establishments = group['number_of_electricity_establishments'].sum()
    number_of_natural_gas_establishments = group['number_of_natural_gas_establishments'].sum()
    business_score = pd.merge(number_of_electricity_establishments, number_of_natural_gas_establishments)
    business_score.rename(columns={'electricity_users':'business'}, inplace=True)

    business_score = pd.merge(business_score, df_business, on='business', how='left')

    # calculate the each city's industry electricity and gas weight
    business_score['elec_score'] = business_score['number_of_electricity_establishments'] * business_score['mean_elec']
    business_score['gas_score'] = business_score['number_of_natural_gas_establishments'] * business_score['mean_gas']

    # drop the useless columns which comes from df_business
    x = [3, 4, 5, 6, 7, 8, 9]
    business_score.drop(business_score.columns[x], axis=1, inplace=True)

    # combine the same city's electricity and gas score
    group2 = business_score.groupby(by=['city','state_abbr'], as_index=False)
    total_elec_score = group2['elec_score'].sum()
    total_gas_score = group2['gas_score'].sum()
    business_score = pd.merge(total_elec_score, total_gas_score)

    print(business_score.shape[0])
    business_score.to_csv("business_score.csv", index=False)

def merge(df_business_scores, df_other):
    df_other.rename(columns={'state_id':'state_abbr'}, inplace=True)

    df_energy1 = pd.merge(df_business_scores, df_other, on=['city','state_abbr'], how='left')
    df_energy = df_energy1.dropna(axis=0, how='any')
    print(df_energy.shape[0])

    df_energy.to_csv("energy_commercial.csv", index=False)

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
