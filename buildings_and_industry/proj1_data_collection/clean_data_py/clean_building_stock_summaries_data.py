# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 5 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Clean building stock summaries data
#     Command:        $python 
#     Note:           Delete row if building count is zero
#                     Assign clearer representation to sector
# ##################################################################

import numpy as np
import pandas as pd
import requests
import json

def get_df(file_name):
    print('Read original data: ')

    # Read original data
    myDataFrame = pd.read_csv(file_name , sep=',', encoding='latin1')
    return myDataFrame

def drop_nan(df):
    # Drop missing-value row
    # Because if there is a mising value in a row
    # It means the building_count must be mising value
    # Then it is not valuable to analysis
    print('Drop row with nan building count: ')
    df=df.dropna()
    return df

def replace_val(df):
    # Poor representation, change to clearer representation
    print('Replace to make cleaner representation: ')
    df=df.replace(to_replace='ind', value='industrial')
    df=df.replace(to_replace='com', value='commercial')
    df=df.replace(to_replace='res', value='residential')
    return df

def export_csv(df):
    print('Export to CSV file with sorting dataframe: ')

    # Sort by zip, city and town
    df=df.sort_values(by=['zip', 'city', 'town'])

    # Export to CSV
    df.to_csv('cleaned_building_stock_summaries_data.csv')
    print('All finished')

if __name__ == "__main__":

    # Read original data
    # Please unzip the original CSV file in data_in_csv folder
    df=get_df('../data_in_csv/building_stock_summaries.csv')

    # Drop missing-value rows
    df=drop_nan(df)

    # Replace unclear values
    df=replace_val(df)

    # Export cleaned data to CSV file
    # This CSV file is zipped
    export_csv(df)
