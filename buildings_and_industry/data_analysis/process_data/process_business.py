# ################################################################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 28 2019
#     Version:        Python 3.7
#     Project 2:      Data analysis
#     Title:          Process business classfication in elec/gas
#     Command:        $python process_business.py
#                     or $run.sh
#
#     Description:    Calculate weight for each business usage amount in total usage amount
#                     New CSV file: commercial_business_analysis.csv  
#                     This CSV file is minor data to analysis in this project
#
#     Note:           *** Please run process_commercial.py to get sub_commercial.cav frist
# ################################################################################################################

import pandas as pd

def read_csv(file_name):

    # Read data
    df=pd.read_csv(file_name, sep=',')
    return df

def get_subset(df):

    # Business classfication
    my_df=pd.DataFrame()

    my_df['naics_3']=df['naics_3']  
    my_df['business']=df['business']

    my_df['electricity_use']=df['electricity_use']
    my_df['natural_gas_use']=df['natural_gas_use']
    my_df=my_df.dropna()
    return my_df


if __name__ == "__main__":

    # Read data
    df=read_csv('sub_commercial.csv')
    print(df.info())

    # Get necessary-features subset
    my_df=get_subset(df)
    print(my_df.info())

    # Calculate total elec/gas usage amount
    total_elec_usage=my_df['electricity_use'].tolist()
    print(sum(total_elec_usage))

    total_gas_usage=my_df['natural_gas_use'].tolist()
    print(sum(total_gas_usage))

    # Process duplicates bu business
    business_df=my_df.groupby(['naics_3', 'business']).sum()

    # Weight of elec/gas usage amount of each business in total elec/gas usage amount
    business_df['weight_of_elec']=business_df['electricity_use']/sum(total_elec_usage)
    business_df['weight_of_gas']=business_df['natural_gas_use']/sum(total_gas_usage)

    # Process key and code to business df
    code=my_df['naics_3'].drop_duplicates().tolist()
    business_df['naics_3']=code

    key=my_df['business'].drop_duplicates().tolist()
    business_df['business']=key


    print(business_df.info())

    business_df.to_csv('commercial_business_analysis.csv', index=False)
