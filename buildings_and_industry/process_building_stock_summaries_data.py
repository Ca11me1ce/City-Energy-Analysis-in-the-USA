# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Oct 2 2019
#     Version:        Python 3.7
#     Project 1:      
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

    attr=[  'city', 
            'state_abbr', 
            'zip', 
            'town',
            'building_type', 
            'building_type_description', 
            'building_count', 
            'total_area_square_foot', 
            'average_building_square_foot', 
            'sector', 
            'area_avg_res', 
            'area_sum_res', 
            'count_sum_res', 
            'area_avg_com', 
            'area_sum_com', 
            'count_sum_com', 
            'area_avg_ind', 
            'area_sum_ind', 
            'count_sum_ind']

    _writer.writerow(attr)
    return _writer

if __name__ == "__main__":
    # Open JSON file
    f_json=open_file('building_stock_summaries.json', 'r')

    # Read content
    # Clean and process JSON data
    _str=f_json.read().strip()
    json_ls=clean_json_data(_str)

    f_csv=open('building_stock_summaries.csv', 'w', newline='') 
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
            town.append(result) # add town

            for activity in json_dict['result'][result]['city_hazus_buildings']:
                info=[]
                info.append(activity['building_type'] if activity['building_type'] else None)
                info.append(activity['building_type_description'] if activity['building_type_description'] else None)
                info.append(activity['building_count'] if activity['building_count'] else None)
                info.append(activity['total_area_square_foot'] if activity['total_area_square_foot'] else None)
                info.append(activity['average_building_square_foot'] if activity['average_building_square_foot'] else None)
                info.append(activity['sector'] if activity['sector'] else None)

                hazus=json_dict['result'][result]['calculated_values']
                info.append(hazus['area_avg_res'] if hazus['area_avg_res'] else None)
                info.append(hazus['area_sum_res'] if hazus['area_sum_res'] else None)
                info.append(hazus['count_sum_res'] if hazus['count_sum_res'] else None)
                info.append(hazus['area_avg_com'] if hazus['area_avg_com'] else None)
                info.append(hazus['area_sum_com'] if hazus['area_sum_com'] else None)
                info.append(hazus['count_sum_com'] if hazus['count_sum_com'] else None)
                info.append(hazus['area_avg_ind'] if hazus['area_avg_ind'] else None)
                info.append(hazus['area_sum_ind'] if hazus['area_sum_ind'] else None)
                info.append(hazus['count_sum_ind'] if hazus['count_sum_ind'] else None)



                new_row=row+town+info
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