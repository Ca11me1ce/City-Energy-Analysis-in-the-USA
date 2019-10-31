# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 2 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Process building disclosures data
#     Command:        $python process_building_disclosures_data.py
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

    try:
        # Remove empty element
        json_ls.remove('')
    except:
        pass

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
            'count_0', 
            'sum_0', 
            'count_5000', 
            'sum_5000', 
            'count_10000', 
            'sum_10000', 
            'count_15000', 
            'sum_15000', 
            'count_20000', 
            'sum_20000', 
            'count_25000', 
            'sum_25000', 
            'count_30000',
            'sum_30000',
            'count_35000',
            'sum_35000',
            'count_40000',
            'sum_40000',
            'count_45000',
            'sum_45000',
            'count_50000',
            'sum_50000',
            'city_name',
            'gisjoin',
            ]

    _writer.writerow(attr)
    return _writer

if __name__ == "__main__":
    # Open JSON file
    f_json=open_file('../data_in_json/building_disclosure.json', 'r')

    # Read content
    # Clean and process JSON data
    _str=f_json.read().strip()
    json_ls=clean_json_data(_str)

    f_csv=open('../data_in_csv/building_disclosure.csv', 'w', newline='') 
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

        try:
            json_dict['result']
        except:
            continue
        
 

        for activity in json_dict['result']['building_disclosures']:
            info=[]
            info.append(activity['type'] if activity['type'] else None)
            info.append(activity['count_0'] if activity['count_0'] else None)
            info.append(activity['sum_0'] if activity['sum_0'] else None)
            info.append(activity['count_5000'] if activity['count_5000'] else None)
            info.append(activity['sum_5000'] if activity['sum_5000'] else None)
            info.append(activity['count_10000'] if activity['count_10000'] else None)
            info.append(activity['sum_10000'] if activity['sum_10000'] else None)
            info.append(activity['count_15000'] if activity['count_15000'] else None)
            info.append(activity['sum_15000'] if activity['sum_15000'] else None)
            info.append(activity['count_20000'] if activity['count_20000'] else None)
            info.append(activity['sum_20000'] if activity['sum_20000'] else None)
            info.append(activity['count_25000'] if activity['count_25000'] else None)
            info.append(activity['sum_25000'] if activity['sum_25000'] else None)
            info.append(activity['count_30000'] if activity['count_30000'] else None)
            info.append(activity['sum_30000'] if activity['sum_30000'] else None)
            info.append(activity['count_35000'] if activity['count_35000'] else None)
            info.append(activity['sum_35000'] if activity['sum_35000'] else None)
            info.append(activity['count_40000'] if activity['count_40000'] else None)
            info.append(activity['sum_40000'] if activity['sum_40000'] else None)
            info.append(activity['count_45000'] if activity['count_45000'] else None)
            info.append(activity['sum_45000'] if activity['sum_45000'] else None)
            info.append(activity['count_50000'] if activity['count_50000'] else None)
            info.append(activity['sum_50000'] if activity['sum_50000'] else None)
            info.append(activity['city_name'] if activity['city_name'] else None)
            info.append(activity['gisjoin'] if activity['gisjoin'] else None)

            new_row=row+info
            if len(new_row)!=28:
                print('Invalid value')
                break
            _writer.writerow(new_row)
            row_num=row_num+1
            print('Number of Insertion: '+str(row_num))
        print('Finish NUMBER OF ZIP: '+str(count))

    f_json.close()
    f_csv.close()

    print('ALL finish')