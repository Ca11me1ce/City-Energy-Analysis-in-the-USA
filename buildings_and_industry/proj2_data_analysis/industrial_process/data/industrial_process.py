import sys
import numpy as np
import pandas as pd
from pprint import pprint

def main(argv):

    # Read Data
    dataFrame = pd.read_csv('cleaned_industrial_data.csv', sep=',', encoding='latin1')
    
    # Drop index column and zipcode
    # Because city and state are enough
    dataFrame = handleDuplicate(dataFrame)

    # Get weight/mean of every business
    df_business = handleTotalBusiness(dataFrame)
    df_business.to_csv('business.csv', index = False)

    # Select most important features
    df_clean = deleteColumn(dataFrame)
    df_clean.to_csv('cleaned_attribute.csv', index=False)

    # Calculate elec/gas score
    df_business_scores = calBusinessScore(df_clean, df_business)
    df_business_scores.to_csv("business_score.csv", index=False)

    # Merge industrial building data and elec/gas data and greenhouse data
    df_other = pd.read_csv('common_attrs_industrial.csv', sep=',', encoding='latin1')
    df_energy = merge(df_business_scores, df_other)
    df_energy.to_csv("energy_industrial.csv", index=False)

def handleDuplicate(dataFrame):

    # Drop index and zip columns
    x = [0, 3]
    dataFrame.drop(dataFrame.columns[x], axis=1, inplace=True)
    dataFrame = dataFrame.drop_duplicates()

    return dataFrame

def handleTotalBusiness(dataFrame):

    # Calculate the mean of elec/gas in every business
    group = dataFrame.groupby(by=['electricity_users'], as_index=False)
    se_group = group.size()
    dict_group = {'electricity_users': se_group.index, 'building_num': se_group.values}
    df_group = pd.DataFrame(dict_group)

    business1 = group['electricity_use_per_establishment'].sum()
    business2 = group['natural_gas_use_per_establishment'].sum()
    business3 = pd.merge(business1, business2)
    business = pd.merge(business3, df_group)
    business.rename(columns={'electricity_users':'business'}, inplace=True)

    business['mean_elec'] = business['electricity_use_per_establishment'] / business['building_num']
    business['mean_gas'] = business['natural_gas_use_per_establishment'] / business['building_num']

    return business

def deleteColumn(dataFrame):

    # Select most important features from raw data
    x = [0, 2, 4, 7, 8, 9, 10, 11, 13, 14, 15, 16]
    dataFrame.drop(dataFrame.columns[x], axis=1, inplace=True)
    dataFrame.rename(columns={'town':'city'}, inplace=True)
    return dataFrame

def calBusinessScore(df_clean, df_business):

    # Calculate business scores
    group = df_clean.groupby(by=['city','state_abbr','electricity_users'], as_index=False)

    # Total buildings
    number_of_electricity_establishments = group['number_of_electricity_establishments'].sum()
    number_of_natural_gas_establishments = group['number_of_natural_gas_establishments'].sum()
    business_score = pd.merge(number_of_electricity_establishments, number_of_natural_gas_establishments)
    business_score.rename(columns={'electricity_users':'business'}, inplace=True)

    business_score = pd.merge(business_score, df_business, on='business', how='left')

    # Business scores
    business_score['elec_score'] = business_score['number_of_electricity_establishments'] * business_score['mean_elec']
    business_score['gas_score'] = business_score['number_of_natural_gas_establishments'] * business_score['mean_gas']

    x = [3, 4, 5, 6, 7, 8, 9]
    business_score.drop(business_score.columns[x], axis=1, inplace=True)

    group2 = business_score.groupby(by=['city','state_abbr'], as_index=False)
    total_elec_score = group2['elec_score'].sum()
    total_gas_score = group2['gas_score'].sum()
    business_score = pd.merge(total_elec_score, total_gas_score)

    return business_score

def merge(df_business_scores, df_other):
    df_other.rename(columns={'state_id':'state_abbr'}, inplace=True)

    df_energy1 = pd.merge(df_business_scores, df_other, on=['city','state_abbr'], how='left')

    df_energy = df_energy1.dropna(axis=0, how='any')

    return df_energy

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
