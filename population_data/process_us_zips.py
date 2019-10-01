# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Sep 30 2019
#     Version:        Python 3.7
#     Project 1:      Clean and process US zips
#     Command:        $python process_us_zips.py
# ##################################################################

import numpy as np
import pandas as pd

def explore_data(file_name):

    # Read data csv
    my_df=pd.read_csv(file_name, sep=',', encoding='latin1')
    return my_df

if __name__ == "__main__":
    state_df=explore_data('us_states.csv')

    # Source comes from https://simplemaps.com/data/us-zips
    zip_df=explore_data('us_zips.csv')

    state_ls=list(state_df['Abbreviation'])

    # Remove rows which are not in USA 50 states
    for i, row in zip_df.iterrows():
        if row['state_id'] not in state_ls:
            zip_df=zip_df.drop(i)
    
    # Build processed csv file of zips
    zip_df.to_csv('processed_us_zips.csv')

