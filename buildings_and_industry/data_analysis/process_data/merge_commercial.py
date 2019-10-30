# ################################################################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 28 2019
#     Version:        Python 3.7
#     Project 2:      Data analysis
#     Title:          Merge commercial data
#     Command:        $python merge_commercial.py
#                     or $run.sh
#
#     Description:    Merge most-importcance features with features from other group members
#                     New CSV file: commercial_analysis.csv  
#                     This CSV file is main data to analysis in this project
#
#     Note:           *** Please run process_commercial.py to get sub_commercial.cav frist
# ################################################################################################################

import pandas as pd

def read_csv(file_name):

    # Read data
    df=pd.read_csv(file_name, sep=',')
    return df

if __name__ == "__main__":

    # Read raw data
    df1=read_csv('sub_commercial.csv')
    df2=read_csv('common_attrs_commercial.csv')

    # Process and remove duplicate columns
    df2=df2.drop(df2.columns[0], axis=1)
    df2['state_abbr']=df2['state_id']
    df2=df2.drop(['state_id'], axis=1)
    print(df1.info())
    print(df2.info())

    # Left join two dataframes
    df=pd.merge(df1, df2, how='left', on=['city', 'state_abbr'])

    # Drop missing values
    # Process duplicates
    df=df.dropna(axis=0)
    df=df.drop_duplicates()

    # Sort rows by zip
    df=df.sort_values(by=['zip'])
    print(df.info())

    # Merge two dataframes to merge all most-important features
    df.to_csv('commercial_analysis.csv', index=False)

