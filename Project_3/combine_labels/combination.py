import sys
import numpy as np
import pandas as pd
from pprint import pprint

def main(sys):
    df_residential = processResidential()
    df_commercial = processCommercial()
    df_industrial = processIndustrial()

    df_energy = mergeDate(df_residential, df_commercial, df_industrial)
    df_energy.to_csv("energy_final.csv", index = False)

    df_energy_class = findClass(df_energy)
    df_energy.to_csv("energy_final_class.csv", index = False)

    countClass(df_energy_class)

def processResidential():
    df_residential = pd.read_csv('degreed_residential.csv' , sep=',', encoding='latin1')
    df_residential.rename(columns={'state_id':'state_abbr', 'housing_units':'r_housing_units', 'total_pop':'r_total_pop', 
                                  'elec_1kdollars':'r_elec_1kdollars', 'elec_mwh':'r_elec_mwh', 'gas_1kdollars':'r_gas_1kdollars',
                                  'gas_mcf':'r_gas_mcf', 'elec_lb_ghg':'r_elec_lb_ghg', 'gas_lb_ghg':'r_gas_lb_ghg',
                                  'elec_degree':'r_elec_class', 'gas_degree':'r_gas_class'
                        }, inplace = True)
    df_residential_city = df_residential.city
    df_residential = df_residential.drop('city', axis = 1)
    df_residential.insert(0, 'city', df_residential_city
    )
    return df_residential

def processCommercial():
    df_commercial = pd.read_csv('labeled_energy_commercial.csv' , sep=',', encoding='latin1')
    attributes = ['elec_class', 'gas_class']
    for attribute in attributes:
        df_commercial.loc[df_commercial[attribute] == 'Normal', attribute] = 1
        df_commercial.loc[df_commercial[attribute] == 'High', attribute] = 2
        df_commercial.loc[df_commercial[attribute] == 'Extremely High', attribute] = 3

    df_commercial.rename(columns={'elec_score':'c_elec_score', 'gas_score':'c_gas_score', 'num_establishments':'c_num_establishments',
                                  'elec_1kdollars':'c_elec_1kdollars', 'elec_mwh':'c_elec_mwh', 'gas_1kdollars':'c_gas_1kdollars',
                                  'gas_mcf':'c_gas_mcf', 'elec_lb_ghg':'c_elec_lb_ghg', 'gas_lb_ghg':'c_gas_lb_ghg',
                                  'elec_class':'c_elec_class', 'gas_class':'c_gas_class'
                        }, inplace = True)
    return df_commercial

def processIndustrial():
    df_industrial = pd.read_csv('cleaned_energy_industrial.csv' , sep=',', encoding='latin1')
    df_industrial.rename(columns={'elec_score':'i_elec_score', 'gas_score':'i_gas_score', 'num_establishments':'i_num_establishments',
                                  'elec_1kdollars':'i_elec_1kdollars', 'elec_mwh':'i_elec_mwh', 'gas_1kdollars':'i_gas_1kdollars',
                                  'gas_mcf':'i_gas_mcf', 'elec_lb_ghg':'i_elec_lb_ghg', 'gas_lb_ghg':'i_gas_lb_ghg',
                                  'elec_bin_group':'i_elec_class', 'gas_bin_group':'i_gas_class'
                        }, inplace = True)

    return df_industrial

def mergeDate(df_residential, df_commercial, df_industrial):
    df_energy = pd.merge(df_residential, df_commercial, on=['city','state_abbr'], how = 'outer')
    df_energy = pd.merge(df_energy, df_industrial, on=['city','state_abbr'], how = 'outer')
    return df_energy

def findClass(df_energy):
    x = [2,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,20,23,24,25,26,27,28,29,30,31]
    df_energy.drop(df_energy.columns[x], axis=1, inplace=True)

    df_energy.fillna(0, inplace = True)

    return df_energy

def countClass(df_energy_class):
    state_group = df_energy_class.groupby(by=['state_abbr'], as_index=False)
    attributes = ['r_elec_class', 'r_gas_class', 'c_elec_class', 'c_gas_class', 'i_elec_class', 'i_gas_class']
    state = []
    for name, group in state_group:
        state.append(name)
    
    data_dict = {}
    for attribute in attributes:
        data = []    
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            className = valueCounts.index[0]
            if className == 0.0 and valueCounts.shape[0] > 1:
                className = valueCounts.index[1]
            data.append(className)
        data_dict[attribute] = data

    data_dict = {'state_abbr': state, 
                 'r_elec_class': data_dict.get('r_elec_class'),
                 'r_gas_class': data_dict.get('r_gas_class'),
                 'c_elec_class': data_dict.get('c_elec_class') ,
                 'c_gas_class': data_dict.get('c_gas_class'),
                 'i_elec_class': data_dict.get('i_elec_class'),
                 'i_gas_class': data_dict.get('i_gas_class')}
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('result.csv', index=False )

if __name__ == "__main__":
    main(sys.argv)