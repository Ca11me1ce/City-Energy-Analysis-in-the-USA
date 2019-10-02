# ##################################################################
#     Author:         Yang Chen
#     NetID:          yc840
#     Modified        Time: Sep 30 2019
#     Version:        Python 3.7
#     Project 1:      
#     API Key:        JQMuffanYBORiUtF8QsrK4aYwi11t6nINWHPRQXt
#                       Qxswuzd7Y7xPUhut4unLixcBvuYJu9enny5kmRiG
#     Command:        $python 
# ##################################################################

import numpy as np
import pandas as pd
import requests
import json
# from ..population_data import process_us_zips



def open_file(file_name):
    f=open(file_name, 'a')
    return f

def explore_data(file_name):

    # Read data csv
    my_df=pd.read_csv(file_name, sep=',', encoding='latin1')
    return my_df

def get_data(api_key, f, zip_code, city, state, t):
    url='https://developer.nrel.gov/api/cleap/v1/activities'
    query_params={
        'city': city,
        'state_abbr': state,
        'zip': str(zip_code),
        'type': t,
        'api_key': api_key
    }

    response=requests.get(url, params=query_params)
    my_dict=json.loads(response.text)
    # if my_dict['errors']!={}

    try:
        if my_dict['error']['code']=='OVER_RATE_LIMIT':
            return 'fail'
    except:
        pass

    f.writelines(response.text+'\n')
    return my_dict


if __name__ == "__main__":

    f=open_file('activities_industrial.json')
    f1=open_file('activities_commercial.json')

    zip_df=explore_data('../population_data/processed_us_zips.csv')
    zip_ls=list(zip_df['zip'])
    city_ls=list(zip_df['city'])
    state_ls=list(zip_df['state_id'])
    api_key=['CD2OojmtzL6fkFJOr8PpfRKriJKdve00T2lJL3dQ', \
        'lbw7uugfKeOVUet66sS4vprzUA5AaoPXjUCQQfQl', \
        'vU0CObhFIruZf96AcUY4ZZd4paP0L6eeO63p0Nc7', \
        '9fgb1saHvLtVjW1n1Gbbf9aFQawkA3diGxgV17hE', \
        'o843dTSd87VmZSvWN9V2oTI5ZKRShOlwJv1p2wmc', \
        'BO0tuWTpxj1yOGVbco8TaaGzmarQxJL2QM2sWPc6', \
        'Yh4IoFgPstLsyjeKhomrv3dk0uo4fYBKuJjAiXNJ', \
        'qYIMJwfAF5udHIew0YOVZX5JHr89czlfmGAr4qid', \
        'il66jtGewVMdxUEqoIU4wg8K4vJgWJ0cLWuqwpmx', \
        'b12xBrVyoQbusvvhCbIVeb0KiUNiRWmoQ4pwluU5', \
        'Mrhnsfa3xtA9hYLrlSxL1Qx6UCH8K7N40KT6dsRI', \
        'yIkp3Nn8AoTS1wOGexdmzlJ8xIkfRUwdRgegW55Y', \
        'r6EExOx96rj9WSgdrMU1LiLCrgn1pbYQFaVlmfqh', \
        'nivobjr83KgFJp9VpMOX8aE43G86EmOOR2nqOxPf', \
        'oxDonHcfaCrCQM4AdameTS5yCIjYIMicFFSMHJaf', \
        'wctTP4lPG6d9yPeQVfUa742fce5Z8uSSjZ40NIPK', \
        'ZKhGBLrlUyUTmudlrAox0ay0AayzWMVR1d7ZamBp', \
        'ZxDUIHf3ghdsQgRRVh4UKkJ4Sn5imxno2dJTPvec', \
        'jMExCBn26t8WCFIdPwbevSzvmogy6oE4AY0PvAEz', \
        'JQMuffanYBORiUtF8QsrK4aYwi11t6nINWHPRQXt', \
        'Qxswuzd7Y7xPUhut4unLixcBvuYJu9enny5kmRiG']

    # zip_ls=[22209]
    # city_ls=['Arlington']
    # state_ls=['VA']
    # {"errors":[{"code":"NOT_FOUND","developer_message":"No data was found for the city/state_abbr or zip, and type provided"}],"inputs":{"city":"Middle Amana","state_abbr":"IA","zip":"52307","type":"commercial"},"metadata":{"version":"1.0.0"}}

    j=0
    key=api_key[0]
    for i in range(0, len(zip_ls)):
        my_df=get_data(key, f, zip_ls[i] if len(str(zip_ls[i]))==5 else '0'+str(zip_ls[i]), city_ls[i], state_ls[i], 'industrial')
        print(my_df)
        my_df=get_data(key, f1, zip_ls[i] if len(str(zip_ls[i]))==5 else '0'+str(zip_ls[i]), city_ls[i], state_ls[i], 'commercial')
        print(my_df)

        if my_df=='fail':
            j=j+1
            if j==len(api_key):
                break
            key=api_key[j]
            continue


    f.close()
    f1.close()
    print('---Finished---')
    print(i)