# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 5 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Clean industrial data
#     Command:        $python 
#     Note:           
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

def export_csv(df, file_name):
    print('Export to CSV file with sorting dataframe: ')

    # Sort by zip, city
    df=df.sort_values(by=['zip', 'city', 'naics_3'])

    # Export to CSV
    df.to_csv(file_name)
    print('All finished')

if __name__ == "__main__":

    # Get original data
    # Please unzip this file first if it is zipped
    df=get_df('../data_in_csv/industrial.csv')

    print('The length of original data: ')
    print(len(df))

    print('The information of original data: ')
    print(df.info())

    # Calculate the fraction of missing values for each attrs
    print('Fraction of missing values: ')
    miss_val=df.isna().sum()
    print(miss_val)
    fraction=miss_val/len(df)
    print(fraction)

    # Export cleaned data to CSV file
    # The file is zipped in github
    export_csv(df, '../cleaned_data_csv/cleaned_industrial_data.csv')
    