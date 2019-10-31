# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 2 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Process lmi housing units data
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
            'id', 
            'bldg_type', 
            'gisjoin', 
            'hu_owner_0_30', 
            'hu_owner_100_plus', 
            'hu_owner_30_50', 
            'hu_owner_50_80', 
            'hu_owner_80_100', 
            'hu_renter_0_30', 
            'hu_renter_100_plus', 
            'hu_renter_30_50', 
            'hu_renter_50_80', 
            'hu_renter_80_100', 
            'name',
            'namelsad',
            'statefp'
            ]

    _writer.writerow(attr)
    return _writer

if __name__ == "__main__":
    # Open JSON file
    f_json=open_file('../data_in_json/lmi_housing_units.json', 'r')

    # Read content
    # Clean and process JSON data
    _str=f_json.read().strip()
    json_ls=clean_json_data(_str)

    f_csv=open('../data_in_csv/lmi_housing_units.csv', 'w', newline='') 
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
        
 

        for activity in json_dict['result']['lmi_housing_units_by_ave_income']:
            info=[]
            info.append(activity['id'] if activity['id'] else None)
            info.append(activity['bldg_type'] if activity['bldg_type'] else None)
            info.append(activity['gisjoin'] if activity['gisjoin'] else None)
            info.append(activity['hu_owner_0_30'] if activity['hu_owner_0_30'] else None)
            info.append(activity['hu_owner_100_plus'] if activity['hu_owner_100_plus'] else None)
            info.append(activity['hu_owner_30_50'] if activity['hu_owner_30_50'] else None)
            info.append(activity['hu_owner_50_80'] if activity['hu_owner_50_80'] else None)
            info.append(activity['hu_owner_80_100'] if activity['hu_owner_80_100'] else None)
            info.append(activity['hu_renter_0_30'] if activity['hu_renter_0_30'] else None)
            info.append(activity['hu_renter_100_plus'] if activity['hu_renter_100_plus'] else None)
            info.append(activity['hu_renter_30_50'] if activity['hu_renter_30_50'] else None)
            info.append(activity['hu_renter_50_80'] if activity['hu_renter_50_80'] else None)
            info.append(activity['hu_renter_80_100'] if activity['hu_renter_80_100'] else None)
            info.append(activity['name'] if activity['name'] else None)
            info.append(activity['namelsad'] if activity['namelsad'] else None)
            info.append(activity['statefp'] if activity['statefp'] else None)

            new_row=row+info
            if len(new_row)!=19:
                print('Invalid value')
                break
            _writer.writerow(new_row)
            row_num=row_num+1
            print('Number of Insertion: '+str(row_num))
        print('Finish NUMBER OF ZIP: '+str(count))

    f_json.close()
    f_csv.close()

    print('ALL finish')