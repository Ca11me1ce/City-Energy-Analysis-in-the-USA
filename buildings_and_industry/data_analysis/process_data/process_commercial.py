# ################################################################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 28 2019
#     Version:        Python 3.7
#     Project 2:      Data analysis
#     Title:          Process raw commercial building data
#     Command:        $python process_commercial.py
#                     or $run.sh
#
#     Description:    Select most importcance features from raw data
#                     Calculate elec/gas weight as a new features
#                     New CSV file: sub_commercial.csv  
#
#     Note:           *** If you download from my GitHub, please unzip commercial_building_csv.zip first,
#                     to get commercial_building.csv file
# ################################################################################################################

import pandas as pd

def read_csv(file_name):

    # Read data
    df=pd.read_csv(file_name, sep=',')
    return df

def get_subset(df):

    # Get most important features from raw data
    my_df=pd.DataFrame()
    my_df['zip']=df['zip']
    my_df['city']=df['city']
    my_df['state_abbr']=df['state_abbr']
    my_df['town']=df['town']
    my_df['type']=df['type']

    # Business classfication
    my_df['naics_3']=df['naics_3']  
    my_df['business']=df['electricity_users']

    # Number of electricity building in this business
    # Total electricity used in this business
    # Average electricity for each building in this business
    my_df['number_of_electricity_establishments']=df['number_of_electricity_establishments']  
    my_df['electricity_use']=df['electricity_use']
    my_df['electricity_use_per_establishment']=df['electricity_use_per_establishment']

    # Number of natural gas building in this business
    # Total natural gas used in this business
    # Average natural gas for each building in this business
    my_df['number_of_natural_gas_establishments']=df['number_of_natural_gas_establishments']
    my_df['natural_gas_use']=df['natural_gas_use']
    my_df['natural_gas_use_per_establishment']=df['natural_gas_use_per_establishment']
    my_df=my_df.dropna()
    return my_df

if __name__ == "__main__":

    # Read raw data
    df=read_csv('commercial_building.csv')
    print(df.info())

    # Get most important features from raw data
    my_df=get_subset(df)

    # Process duplicates by city and state_abbr
    my_df=my_df.drop_duplicates(subset=['city', 'state_abbr', 'town'], keep='first')
    print(my_df.info())

    

    # Calculate total elec/gas usage amount
    total_elec_usage=my_df['electricity_use'].tolist()
    print(sum(total_elec_usage))

    total_gas_usage=my_df['natural_gas_use'].tolist()
    print(sum(total_gas_usage))

    # Weight of each business elec/gas usage amount of one town in total elec/gas usage amount
    my_df['weight_of_elec']=my_df['electricity_use']/sum(total_elec_usage)
    my_df['weight_of_gas']=my_df['natural_gas_use']/sum(total_elec_usage)

    print(my_df['weight_of_elec'].describe())
    print(my_df['weight_of_gas'].describe())

    my_df=my_df.sort_values(by=['zip'])

    # Select most importance features from commercial building csv
    # These features will much impact our analysis
    # And use these features to calculate other important features
    my_df.to_csv('sub_commercial.csv', index=False)

    


