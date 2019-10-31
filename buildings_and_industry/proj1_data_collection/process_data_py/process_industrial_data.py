# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 2 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Process industrial data
#     Command:        $python 
# ##################################################################
import numpy as np
import pandas as pd
import requests
import json
import csv
from ast import literal_eval

def open_file(file_name, q):
    f=open(file_name, q)
    return f

def clean_json_data(_str):

    # Remove duplication
    json_ls=list(set(_str.split('\n')))

    # Remove empty element
    json_ls.remove('')

    for i in json_ls:
        if '"code":"NOT_FOUND"' in i:
            json_ls.remove(i)

    return json_ls
    
def define_csv_file(f):
    _writer=csv.writer(f, delimiter=',')

    attr=['city', 
            'state_abbr', 
            'zip', 
            'type', 
            'town', 
            'naics_3', 
            'electricity_users', 
            'number_of_electricity_establishments', 
            'electricity_use', 
            'rank_of_electricity_use', 
            'electricity_use_per_establishment', 
            'rank_of_electricity_use_per_establishment', 
            'natural_gas_users', 
            'number_of_natural_gas_establishments', 
            'natural_gas_use', 
            'rank_of_natural_gas_use', 
            'natural_gas_use_per_establishment', 
            'rank_of_natural_gas_use_per_establishment']

    _writer.writerow(attr)
    return _writer

if __name__ == "__main__":
    # Open JSON file
    # Please unzip activities_industrial_json.zip to obain the JSON file
    f_json=open_file('../data_in_json/activities_industrial.json', 'r')

    # Read content
    # Clean and process JSON data
    _str=f_json.read().strip()
    json_ls=clean_json_data(_str)

    f_csv=open('../data_in_csv/industrial.csv', 'w', newline='') 
    _writer=define_csv_file(f_csv)
    

    count=0
    row_num=0
    for _json in json_ls:
        count=count+1
        row=[]

        try:
            json_dict=literal_eval(_json)
        except:
            continue
        row.append(json_dict['inputs']['city'])
        row.append(json_dict['inputs']['state_abbr'])
        row.append(json_dict['inputs']['zip'])
        row.append(json_dict['inputs']['type'])

        try:
            json_dict['result']
        except:
            continue
        
        for result in json_dict['result']:
            town=[]
            town.append(result)

            for activity in json_dict['result'][result]['activities']:
                info=[]
                info.append(activity['naics_3'] if activity['naics_3'] else None)
                info.append(activity['electricity_users'] if activity['electricity_users'] else None)
                info.append(activity['number_of_electricity_establishments'] if activity['number_of_electricity_establishments'] else None)
                info.append(activity['electricity_use'] if activity['electricity_use'] else None)
                info.append(activity['rank_of_electricity_use'] if activity['rank_of_electricity_use'] else None)
                info.append(activity['electricity_use_per_establishment'] if activity['electricity_use_per_establishment'] else None)
                info.append(activity['rank_of_electricity_use_per_establishment'] if activity['rank_of_electricity_use_per_establishment'] else None)
                info.append(activity['natural_gas_users'] if activity['natural_gas_users'] else None)
                info.append(activity['number_of_natural_gas_establishments'] if activity['number_of_natural_gas_establishments'] else None)
                info.append(activity['natural_gas_use'] if activity['natural_gas_use'] else None)
                info.append(activity['rank_of_natural_gas_use'] if activity['rank_of_natural_gas_use'] else None)
                info.append(activity['natural_gas_use_per_establishment'] if activity['natural_gas_use_per_establishment'] else None)
                info.append(activity['rank_of_natural_gas_use_per_establishment'] if activity['rank_of_natural_gas_use_per_establishment'] else None)

                new_row=row+town+info
                if len(new_row)!=18:
                    print('Invalid value')
                    break
                _writer.writerow(new_row)
                row_num=row_num+1
                print('Number of Insertion: '+str(row_num))
        print('Finish NUMBER OF ZIP: '+str(count))

    f_json.close()
    f_csv.close()

    print('ALL finish')