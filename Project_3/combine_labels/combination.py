#######################
# Author: Jiexin Kong
# NetID: jk2145
# Function: ccombine three datasets, generate the overall labels for each state.
# ####################
import sys
import numpy as np
import pandas as pd
from pprint import pprint

def main(sys):
    # read three files and transform them into same format
    df_residential = processResidential()
    df_residential.to_csv("final_residential.csv", index = False)
    df_commercial = processCommercial()
    df_commercial.to_csv("final_commercial.csv", index = False)
    df_industrial = processIndustrial()
    df_industrial.to_csv("final_industrial.csv", index = False)

    # combine three dataset
    df_energy = mergeDate(df_residential, df_commercial, df_industrial)
    df_energy.to_csv("energy_final.csv", index = False)

    # extract the labels
    df_energy_class = findClass(df_energy)
    df_energy.to_csv("energy_final_class.csv", index = False)

    # calculate the labels percentage and generate the overall labels for each state
    df_percent = calClassPercentage(df_energy_class)
    dict_RC = calRCClass(df_percent)
    dict_I = calIClass(df_energy_class)
    generateClass(dict_RC, dict_I)

def processResidential():
    df_residential = pd.read_csv('degreed_residential.csv' , sep=',', encoding='latin1')
    # rename the columns
    df_residential.rename(columns={'state_id':'state_abbr', 'housing_units':'r_housing_units', 'total_pop':'r_total_pop', 
                                  'elec_1kdollars':'r_elec_1kdollars', 'elec_mwh':'r_elec_mwh', 'gas_1kdollars':'r_gas_1kdollars',
                                  'gas_mcf':'r_gas_mcf', 'elec_lb_ghg':'r_elec_lb_ghg', 'gas_lb_ghg':'r_gas_lb_ghg',
                                  'elec_degree':'r_elec_class', 'gas_degree':'r_gas_class'
                        }, inplace = True)
    # exchange the columns order
    df_residential_city = df_residential.city
    df_residential = df_residential.drop('city', axis = 1)
    df_residential.insert(0, 'city', df_residential_city
    )
    return df_residential

def processCommercial():
    df_commercial = pd.read_csv('labeled_energy_commercial.csv' , sep=',', encoding='latin1')
    # rename the class labels
    attributes = ['elec_class', 'gas_class']
    for attribute in attributes:
        df_commercial.loc[df_commercial[attribute] == 'Normal', attribute] = 1
        df_commercial.loc[df_commercial[attribute] == 'High', attribute] = 2
        df_commercial.loc[df_commercial[attribute] == 'Extremely High', attribute] = 3

    # rename the columns
    df_commercial.rename(columns={'elec_score':'c_elec_score', 'gas_score':'c_gas_score', 'num_establishments':'c_num_establishments',
                                  'elec_1kdollars':'c_elec_1kdollars', 'elec_mwh':'c_elec_mwh', 'gas_1kdollars':'c_gas_1kdollars',
                                  'gas_mcf':'c_gas_mcf', 'elec_lb_ghg':'c_elec_lb_ghg', 'gas_lb_ghg':'c_gas_lb_ghg',
                                  'elec_class':'c_elec_class', 'gas_class':'c_gas_class'
                        }, inplace = True)
    return df_commercial

def processIndustrial():
    df_industrial = pd.read_csv('cleaned_energy_industrial.csv' , sep=',', encoding='latin1')
    # rename the columns
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
    # extract the labels
    x = [2,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,20,23,24,25,26,27,28,29,30,31]
    df_energy.drop(df_energy.columns[x], axis=1, inplace=True)

    # if the city doesn't have corresponding label, fill in 0
    df_energy.fillna(0, inplace = True)

    return df_energy

def calClassPercentage(df_energy_class):
    state_group = df_energy_class.groupby(by=['state_abbr'], as_index=False)
    attributes = ['r_elec_class', 'r_gas_class', 'c_elec_class', 'c_gas_class', 'i_elec_class', 'i_gas_class']
    # attributes = ['i_elec_class']
    # extract the state name
    state = []
    for name, group in state_group:
        state.append(name)
    
    # calculate the percentage of labels in each class and state
    data_dict = {}
    for attribute in attributes:
        dataNormal = [] 
        dataHigh = []
        dataVeryHigh = []   
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            dict_value = {'className': valueCounts.index, 'classNum': valueCounts.values}
            df_value = pd.DataFrame(dict_value)
            df_value = df_value[~df_value['className'].isin([0])]
            totalNum = df_value['classNum'].sum()
            normal = df_value[df_value['className'] == 1]['classNum']
            if normal.shape[0] == 1:
                normal = normal.iloc[0] / totalNum 
            else:
                normal = 0
            dataNormal.append('%.2f' % normal)
            high = df_value[df_value['className'] == 2]['classNum']
            if high.shape[0] == 1:
                high = high.iloc[0] / totalNum 
            else:
                high = 0
            dataHigh.append('%.2f' % high)
            veryHigh = df_value[df_value['className'] == 3]['classNum']
            if veryHigh.shape[0] == 1:
                veryHigh = veryHigh.iloc[0] / totalNum 
            else:
                veryHigh = 0
            dataVeryHigh.append('%.2f' % veryHigh)
        data_dict[attribute + '_Normal'] = dataNormal
        data_dict[attribute + '_High'] = dataHigh
        data_dict[attribute + '_VeryHigh'] = dataVeryHigh

    # generate the dataframe
    data_dict = {'state_abbr': state, 
                 'r_elec_class_Normal': data_dict.get('r_elec_class_Normal'),
                 'r_elec_class_High': data_dict.get('r_elec_class_High'),
                 'r_elec_class_VeryHigh': data_dict.get('r_elec_class_VeryHigh'),
                 'r_gas_class_Normal': data_dict.get('r_gas_class_Normal'),
                 'r_gas_class_High': data_dict.get('r_gas_class_High'),
                 'r_gas_class_VeryHigh': data_dict.get('r_gas_class_VeryHigh'),
                 'c_elec_class_Normal': data_dict.get('c_elec_class_Normal') ,
                 'c_elec_class_High': data_dict.get('c_elec_class_High') ,
                 'c_elec_class_VeryHigh': data_dict.get('c_elec_class_VeryHigh') ,
                 'c_gas_class_Normal': data_dict.get('c_gas_class_Normal'),
                 'c_gas_class_High': data_dict.get('c_gas_class_High'),
                 'c_gas_class_VeryHigh': data_dict.get('c_gas_class_VeryHigh'),
                 'i_elec_class_Normal': data_dict.get('i_elec_class_Normal'),
                 'i_elec_class_High': data_dict.get('i_elec_class_High'),
                 'i_elec_class_VeryHigh': data_dict.get('i_elec_class_VeryHigh'),
                 'i_gas_class_Normal': data_dict.get('i_gas_class_Normal'),
                 'i_gas_class_High': data_dict.get('i_gas_class_High'),
                 'i_gas_class_VeryHigh': data_dict.get('i_gas_class_VeryHigh')
                 }
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('class_state_percentage.csv', index=False)
    return dict_df

def calRCClass(df_percent):
    dict_class = []
    state = []
    r_e_class = []
    r_g_class = []
    c_e_class = []
    c_g_class = []
    # Assign Labels based on the percentage of classification residential and commercial
    # If the high percentage is larger than 0.2, this state's level is high
    # If the very high percentage is larger than 0.1 and also larger than its high percentage,
    # then this state's level is very high
    for index, row in df_percent.iterrows():
        r_e = 'null'
        r_g = 'null'
        c_e = 'null'
        c_g = 'null'
        state.append(row['state_abbr'])

        if float(row['r_elec_class_Normal']) > 0.4:
            r_e = 'Normal'
        if float(row['r_elec_class_High']) > 0.2:
            r_e = 'High'
        if (float(row['r_elec_class_VeryHigh']) > 0.1) & (float(row['r_elec_class_VeryHigh']) > float(row['r_elec_class_High'])):
            r_e = 'Very High'
        r_e_class.append(r_e)

        if float(row['r_gas_class_Normal']) > 0.4:
            r_g = 'Normal'
        if float(row['r_gas_class_High']) > 0.2:
            r_g = 'High'
        if (float(row['r_gas_class_VeryHigh']) > 0.1) & (float(row['r_gas_class_VeryHigh']) > float(row['r_gas_class_High'])):
            r_g = 'Very High'
        r_g_class.append(r_g)

        if float(row['c_elec_class_Normal']) > 0.4:
            c_e = 'Normal'
        if float(row['c_elec_class_High']) > 0.2:
            c_e = 'High'
        if (float(row['c_elec_class_VeryHigh']) > 0.1) & (float(row['c_elec_class_VeryHigh']) > float(row['c_elec_class_High'])):
            c_e = 'Very High'
        c_e_class.append(c_e)

        if float(row['c_gas_class_Normal']) > 0.4:
            c_g = 'Normal'
        if float(row['r_gas_class_High']) > 0.2:
            c_g = 'High'
        if (float(row['r_gas_class_VeryHigh']) > 0.1) & (float(row['c_gas_class_VeryHigh']) > float(row['c_gas_class_High'])):
            c_g = 'Very High'
        c_g_class.append(c_g)

    dict_class = {
        'state_abbr' : state,
        'r_elec_class': r_e_class,
        'r_gas_class': r_g_class,
        'c_elec_class': c_e_class,
        'c_gas_class': c_g_class
    }

    return dict_class

def calIClass(df_energy_class):
    # this method is used to generate labels for industrial classification
    state_group = df_energy_class.groupby(by=['state_abbr'], as_index=False)
    attributes = ['i_elec_class', 'i_gas_class']
    
    # extract the maximum number of labels in each class and state
    data_dict = {}
    for attribute in attributes:
        data = []    
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            className = int(valueCounts.index[0])
            if className == 0 and valueCounts.shape[0] > 1:
                className = int(valueCounts.index[1])
            data.append(className)
        data_dict[attribute] = data

    # generate the dataframe
    data_dict = {'i_elec_class': data_dict.get('i_elec_class'),
                 'i_gas_class': data_dict.get('i_gas_class')}
    return data_dict

def generateClass(dict_RC, dict_I):
    # combine the industrial labels into commercial and residential label dictionary
    dict_RC['i_elec_class'] = dict_I.get('i_elec_class')
    dict_RC['i_gas_class'] = dict_I.get('i_gas_class')
    dict_df = pd.DataFrame(dict_RC)
    # change the label from number into text
    attributes = ['i_elec_class', 'i_gas_class']
    for attribute in attributes:
        dict_df.loc[dict_df[attribute] == 0, attribute] = 'null'
        dict_df.loc[dict_df[attribute] == 1, attribute] = 'Normal'
        dict_df.loc[dict_df[attribute] == 2, attribute] = 'High'
        dict_df.loc[dict_df[attribute] == 3, attribute] = 'Very High'

    # These codes can check the number of each level of each class 
    # print((dict_df['r_elec_class']).value_counts())
    # print((dict_df['r_gas_class']).value_counts())
    # print((dict_df['c_elec_class']).value_counts())
    # print((dict_df['c_gas_class']).value_counts())
    # print((dict_df['i_elec_class']).value_counts())
    # print((dict_df['i_gas_class']).value_counts())
    dict_df.to_csv('state_class.csv', index=False)

if __name__ == "__main__":
    main(sys.argv)