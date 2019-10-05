# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 2 2019
#     Version:        Python 3.7
#     Project 1:      Collect and Process Data
#     Title:          Process small building pv data
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
    try:
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
            'town', 
            'count', 
            'percent_suitable', 
            'avg_generation_kwh', 
            'avg_generation_kwh_suitable', 
            'area_total_m2', 
            'capacity_total_kw', 
            'energy_total_kwh', 
            'suitable_small_buildings', 
            'unsuitable_small_buildings', 
            'energy_total_mwh', 
            ]

    _writer.writerow(attr)
    return _writer

if __name__ == "__main__":
    # Open JSON file
    f_json=open_file('../data_in_json/small_building_pv.json', 'r')

    # Read content
    # Clean and process JSON data
    _str=f_json.read().strip()
    json_ls=clean_json_data(_str)

    f_csv=open('../data_in_csv/small_building_pv.csv', 'w', newline='') 
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
        
        for result in json_dict['result']:
            town=[]
            town.append(result)

            info=[]
            for activity in json_dict['result'][result]['city_rooftop_solar']:                
                info.append(json_dict['result'][result]['city_rooftop_solar'][activity])
                # info.append(activity['count'] if activity['count'] else None)
                # info.append(activity['percent_suitable'] if activity['percent_suitable'] else None)
                # info.append(activity['avg_generation_kwh'] if activity['avg_generation_kwh'] else None)
                # info.append(activity['avg_generation_kwh_suitable'] if activity['avg_generation_kwh_suitable'] else None)
                # info.append(activity['area_total_m2'] if activity['area_total_m2'] else None)
                # info.append(activity['capacity_total_kw'] if activity['capacity_total_kw'] else None)
                # info.append(activity['energy_total_kwh'] if activity['energy_total_kwh'] else None)
                # info.append(activity['suitable_small_buildings'] if activity['suitable_small_buildings'] else None)
                # info.append(activity['unsuitable_small_buildings'] if activity['unsuitable_small_buildings'] else None)
                # info.append(activity['energy_total_mwh'] if activity['energy_total_mwh'] else None)

            new_row=row+town+info
            if len(new_row)!=14:
                print('Invalid value')
                break
            _writer.writerow(new_row)
            row_num=row_num+1
            print('Number of Insertion: '+str(row_num))
        print('Finish NUMBER OF ZIP: '+str(count))

    f_json.close()
    f_csv.close()

    print('ALL finish')