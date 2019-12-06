#######################
# Author: Jiexin Kong
# NetID: jk2145
# Function: Handle the dataframe and plot.
# ####################
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pprint import pprint

def main(sys):
    # change the lable from int to str which used for plot
    df_residential = readResidential()
    df_residential.to_csv("final_class_residential.csv", index=False)
    df_commercial = readCommercial()
    df_commercial.to_csv("final_class_commercial.csv", index=False)
    df_industrial = readIndustrial()
    df_industrial.to_csv("final_class_industrial.csv", index=False)
    df_state = readState()
    df_state.to_csv("final_class_state.csv", index=False)

    # calculate the averge energy usage for each attribute in every state(used for d3 plot)
    combineResidentialData(df_residential)
    combineCommercialData(df_commercial)
    combineIndustrialData(df_industrial)

    # change the dataframe structure and use new dataframe to draw plotly plot.
    residentialVisual(df_residential)
    commercialVisual(df_commercial)
    industrialVisual(df_industrial)

def readResidential():
    df_residential = pd.read_csv('final_residential.csv' , sep=',', encoding='latin1')
    attributes = ['r_elec_class', 'r_gas_class']
    for attribute in attributes:
        df_residential.loc[df_residential[attribute] == 1, attribute] = 'Normal'
        df_residential.loc[df_residential[attribute] == 2, attribute] = 'High'
        df_residential.loc[df_residential[attribute] == 3, attribute] = 'Very High'
    return df_residential

def readCommercial():
    df_commercial = pd.read_csv('final_commercial.csv' , sep=',', encoding='latin1')
    attributes = ['c_elec_class', 'c_gas_class']
    for attribute in attributes:
        df_commercial.loc[df_commercial[attribute] == 1, attribute] = 'Normal'
        df_commercial.loc[df_commercial[attribute] == 2, attribute] = 'High'
        df_commercial.loc[df_commercial[attribute] == 3, attribute] = 'Very High'
    return df_commercial

def readIndustrial():
    df_industrial = pd.read_csv('final_industrial.csv' , sep=',', encoding='latin1')
    attributes = ['i_elec_class', 'i_gas_class']
    for attribute in attributes:
        df_industrial.loc[df_industrial[attribute] == 1, attribute] = 'Normal'
        df_industrial.loc[df_industrial[attribute] == 2, attribute] = 'High'
        df_industrial.loc[df_industrial[attribute] == 3, attribute] = 'Very High'
    return df_industrial

def readState():
    df_state = pd.read_csv('class_state.csv' , sep=',', encoding='latin1')
    attributes = ['r_elec_class', 'r_gas_class', 'c_elec_class', 'c_gas_class', 'i_elec_class', 'i_gas_class']
    for attribute in attributes:
        df_state.loc[df_state[attribute] == 0, attribute] = 'null'
        df_state.loc[df_state[attribute] == 1, attribute] = 'Normal'
        df_state.loc[df_state[attribute] == 2, attribute] = 'High'
        df_state.loc[df_state[attribute] == 3, attribute] = 'Very High'
    return df_state

def combineResidentialData(df_residential):
    state_group = df_residential.groupby(by=['state_abbr'], as_index=False)
    numeric_attributes = ['r_housing_units', 'r_total_pop', 'r_elec_1kdollars', 
                          'r_elec_mwh', 'r_gas_1kdollars', 'r_gas_mcf', 'r_elec_lb_ghg', 'r_gas_lb_ghg']
    class_attributes = ['r_elec_class', 'r_gas_class']
    # extract the state name
    state = []
    for name, group in state_group:
        state.append(name)
    
    # extract the maximum number of labels in each class and state
    data_dict = {}
    for attribute in class_attributes:
        data = []    
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            className = valueCounts.index[0]
            data.append(className)
        data_dict[attribute] = data

    for attribute in numeric_attributes:
        data = []
        for name, group in state_group:
            valueAvg = group[attribute].mean()
            data.append('%.2f' % valueAvg)
        data_dict[attribute] = data

    # generate the dataframe
    data_dict = {'state_abbr': state, 
                 'r_elec_score': data_dict.get('r_elec_score') ,
                 'r_gas_score': data_dict.get('r_gas_score'),
                 'r_num_establishments': data_dict.get('r_num_establishments') ,
                 'r_elec_1kdollars': data_dict.get('r_elec_1kdollars'),
                 'r_elec_mwh': data_dict.get('r_elec_mwh') ,
                 'r_gas_1kdollars': data_dict.get('r_gas_1kdollars'),
                 'r_gas_mcf': data_dict.get('r_gas_mcf') ,
                 'r_elec_lb_ghg': data_dict.get('r_elec_lb_ghg'),
                 'r_gas_lb_ghg': data_dict.get('r_gas_lb_ghg'),
                 'r_elec_class': data_dict.get('r_elec_class') ,
                 'r_gas_class': data_dict.get('r_gas_class')}
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('state_residential.csv', index=False)
    data_dict1 = {'state_abbr': state, 
                 'r_elec_mwh': data_dict.get('r_elec_mwh')}
    dict_df1 = pd.DataFrame(data_dict1)
    dict_df1.to_csv('state_residential1.csv', sep = ' ', index=False)
    data_dict2 = {'state_abbr': state, 
                  'r_gas_mcf': data_dict.get('r_gas_mcf')}
    dict_df2 = pd.DataFrame(data_dict2)
    dict_df2.to_csv('state_residential2.csv', sep = ' ', index=False)
    return dict_df

def combineCommercialData(df_commercial):
    state_group = df_commercial.groupby(by=['state_abbr'], as_index=False)
    numeric_attributes = ['c_elec_score', 'c_gas_score', 'c_num_establishments', 'c_elec_1kdollars', 
                          'c_elec_mwh', 'c_gas_1kdollars', 'c_gas_mcf', 'c_elec_lb_ghg', 'c_gas_lb_ghg']
    class_attributes = ['c_elec_class', 'c_gas_class']
    # extract the state name
    state = []
    for name, group in state_group:
        state.append(name)
    
    # extract the maximum number of labels in each class and state
    data_dict = {}
    for attribute in class_attributes:
        data = []    
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            className = valueCounts.index[0]
            data.append(className)
        data_dict[attribute] = data

    for attribute in numeric_attributes:
        data = []
        for name, group in state_group:
            valueAvg = group[attribute].mean()
            data.append('%.2f' % valueAvg)
        data_dict[attribute] = data

    # generate the dataframe
    data_dict = {'state_abbr': state, 
                 'c_elec_score': data_dict.get('c_elec_score') ,
                 'c_gas_score': data_dict.get('c_gas_score'),
                 'c_num_establishments': data_dict.get('c_num_establishments') ,
                 'c_elec_1kdollars': data_dict.get('c_elec_1kdollars'),
                 'c_elec_mwh': data_dict.get('c_elec_mwh') ,
                 'c_gas_1kdollars': data_dict.get('c_gas_1kdollars'),
                 'c_gas_mcf': data_dict.get('c_gas_mcf') ,
                 'c_elec_lb_ghg': data_dict.get('c_elec_lb_ghg'),
                 'c_gas_lb_ghg': data_dict.get('c_gas_lb_ghg'),
                 'c_elec_class': data_dict.get('c_elec_class') ,
                 'c_gas_class': data_dict.get('c_gas_class')}
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('state_commercial.csv', index=False)
    data_dict1 = {'state_abbr': state, 
                 'c_elec_mwh': data_dict.get('c_elec_mwh')}
    dict_df1 = pd.DataFrame(data_dict1)
    dict_df1.to_csv('state_commercial1.csv', sep = ' ', index=False)
    data_dict2 = {'state_abbr': state, 
                  'c_gas_mcf': data_dict.get('c_gas_mcf')}
    dict_df2 = pd.DataFrame(data_dict2)
    dict_df2.to_csv('state_commercial2.csv', sep = ' ', index=False)
    return dict_df

def combineIndustrialData(df_industrial):
    state_group = df_industrial.groupby(by=['state_abbr'], as_index=False)
    numeric_attributes = ['i_elec_score', 'i_gas_score', 'i_num_establishments', 'i_elec_1kdollars', 
                          'i_elec_mwh', 'i_gas_1kdollars', 'i_gas_mcf', 'i_elec_lb_ghg', 'i_gas_lb_ghg']
    class_attributes = ['i_elec_class', 'i_gas_class']
    # extract the state name
    state = []
    for name, group in state_group:
        state.append(name)
    
    # extract the maximum number of labels in each class and state
    data_dict = {}
    for attribute in class_attributes:
        data = []    
        for name, group in state_group:
            valueCounts = group[attribute].value_counts()
            className = valueCounts.index[0]
            data.append(className)
        data_dict[attribute] = data

    for attribute in numeric_attributes:
        data = []
        for name, group in state_group:
            valueAvg = group[attribute].mean()
            data.append('%.2f' % valueAvg)
        data_dict[attribute] = data

    # generate the dataframe
    data_dict = {'state_abbr': state, 
                 'i_elec_score': data_dict.get('i_elec_score') ,
                 'i_gas_score': data_dict.get('i_gas_score'),
                 'i_num_establishments': data_dict.get('i_num_establishments') ,
                 'i_elec_1kdollars': data_dict.get('i_elec_1kdollars'),
                 'i_elec_mwh': data_dict.get('i_elec_mwh') ,
                 'i_gas_1kdollars': data_dict.get('i_gas_1kdollars'),
                 'i_gas_mcf': data_dict.get('i_gas_mcf') ,
                 'i_elec_lb_ghg': data_dict.get('i_elec_lb_ghg'),
                 'i_gas_lb_ghg': data_dict.get('i_gas_lb_ghg'),
                 'i_elec_class': data_dict.get('i_elec_class') ,
                 'i_gas_class': data_dict.get('i_gas_class')}
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('state_industrial.csv', index=False)
    data_dict1 = {'state_abbr': state, 
                 'i_elec_mwh': data_dict.get('i_elec_mwh')}
    dict_df1 = pd.DataFrame(data_dict1)
    dict_df1.to_csv('state_industrial1.csv', sep = ' ', index=False)
    data_dict2 = {'state_abbr': state, 
                  'i_gas_mcf': data_dict.get('i_gas_mcf')}
    dict_df2 = pd.DataFrame(data_dict2)
    dict_df2.to_csv('state_industrial2.csv', sep = ' ', index=False)
    return dict_df

def residentialVisual(df_residential):
    residentialElec(df_residential)
    residentialGas(df_residential)

def residentialElec(df_residential):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_residential.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_housing_units')
        value.append(float(row['r_housing_units'])*10000)
        dataclass.append(row['r_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_total_pop')
        value.append(float(row['r_total_pop'])*5000)
        dataclass.append(row['r_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_elec_1kdollars')
        value.append(float(row['r_elec_1kdollars'])*10000)
        dataclass.append(row['r_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_elec_lb_ghg')
        value.append(row['r_elec_lb_ghg'])
        dataclass.append(row['r_elec_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_residential_elec.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             notched=True, # used notched shape
             title="Box plot of residential electricity"
            )
    fig.show()

def residentialGas(df_residential):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_residential.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_housing_units')
        value.append(float(row['r_housing_units'])*10000)
        dataclass.append(row['r_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_total_pop')
        value.append(float(row['r_total_pop'])*5000)
        dataclass.append(row['r_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_gas_1kdollars')
        value.append(float(row['r_gas_1kdollars'])*10000)
        dataclass.append(row['r_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('r_gas_lb_ghg')
        value.append(row['r_gas_lb_ghg'])
        dataclass.append(row['r_gas_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_residential_gas.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             notched=True, # used notched shape
             title="Box plot of residential electricity"
            )
    fig.show()

def commercialVisual(df_commercial):
    commercialElec(df_commercial)
    commercialGas(df_commercial)

def commercialElec(df_commercial):
    #commercialElecVisual1(df_commercial)
    commercialElecVisual2(df_commercial)

def commercialElecVisual1(df_commercial):
    fig = px.scatter(df_commercial, x="c_elec_mwh", y="c_elec_1kdollars", color="c_elec_class", marginal_x="box", trendline="ols")
    fig.show()

def commercialElecVisual2(df_commercial):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_commercial.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_elec_score')
        value.append(float(row['c_elec_score'])*500)
        dataclass.append(row['c_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_num_establishments')
        value.append(float(row['c_num_establishments'])*100000)
        dataclass.append(row['c_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_elec_1kdollars')
        value.append(float(row['c_elec_1kdollars'])*10000)
        dataclass.append(row['c_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_elec_lb_ghg')
        value.append(row['c_elec_lb_ghg'])
        dataclass.append(row['c_elec_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_commercial_elec.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             notched=True, # used notched shape
             title="Box plot of commercial electricity"
            )
    fig.show()

def commercialGas(df_commercial):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_commercial.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_gas_score')
        value.append(float(row['c_gas_score'])*100)
        dataclass.append(row['c_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_num_establishments')
        value.append(float(row['c_num_establishments'])*50000)
        dataclass.append(row['c_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_gas_1kdollars')
        value.append(float(row['c_gas_1kdollars'])*10000)
        dataclass.append(row['c_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('c_gas_lb_ghg')
        value.append(row['c_gas_lb_ghg'])
        dataclass.append(row['c_gas_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_commercial_gas.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             notched=True, # used notched shape
             title="Box plot of commercial natural gas"
            )
    fig.show()   
    
def industrialVisual(df_industrial):
    # # list the attributes which are needed to be processed
    # attributes = ['i_elec_score','i_gas_score','i_num_establishments', 'i_elec_1kdollars', 
    #               'i_elec_mwh', 'i_gas_1kdollars', 'i_gas_mcf', 'i_elec_lb_ghg','i_gas_lb_ghg']

    # # use boxplot to identify outliers
    # boxplot= df_industrial.iloc[:, 2:].boxplot(return_type='dict')

    # for i in range(0, 9):
    #     outliers = boxplot['fliers'][i].get_ydata()
    #     outliers.tolist()
    #     # obtain the corresponding maximum 
    #     mean = df_industrial[attributes[i]].mean()
    #     # replace the outliers with maximum 
    #     df_industrial.loc[df_industrial[attributes[i]].isin(outliers), attributes[i]] = mean

    industrialElec(df_industrial)
    industrialGas(df_industrial)

def industrialElec(df_industrial):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_industrial.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_elec_score')
        value.append(float(row['i_elec_score'])*1000)
        dataclass.append(row['i_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_num_establishments')
        value.append(float(row['i_num_establishments'])*500000)
        dataclass.append(row['i_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_elec_1kdollars')
        value.append(float(row['i_elec_1kdollars'])*10000)
        dataclass.append(row['i_elec_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_elec_lb_ghg')
        value.append(row['i_elec_lb_ghg'])
        dataclass.append(row['i_elec_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_industrial_elec.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             #notched=True, # used notched shape
             title="Box plot of industrial electricity"
            )
    fig.show()

def industrialGas(df_industrial):
    city = []
    state = []
    datatype = []
    value = []
    dataclass = []
    for index, row in df_industrial.iterrows():
        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_gas_score')
        value.append(float(row['i_gas_score'])*50)
        dataclass.append(row['i_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_num_establishments')
        value.append(float(row['i_num_establishments'])*100000)
        dataclass.append(row['i_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_gas_1kdollars')
        value.append(float(row['i_gas_1kdollars'])*10000)
        dataclass.append(row['i_gas_class'])

        city.append(row['city'])
        state.append(row['state_abbr'])
        datatype.append('i_gas_lb_ghg')
        value.append(row['i_gas_lb_ghg'])
        dataclass.append(row['i_gas_class'])

    dict_data = {
        'city': city,
        'state': state,
        'type': datatype,
        'value': value,
        'dataclass': dataclass
    }

    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv("box_industrial_gas.csv", index=False)

    fig = px.box(dict_df, x="type", y="value", color="dataclass",
             #notched=True, # used notched shape
             title="Box plot of industrial natural gas"
            )
    fig.show()

if __name__ == "__main__":
    main(sys.argv)