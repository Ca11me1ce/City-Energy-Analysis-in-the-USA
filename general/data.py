# ##################################################################
#     Author:         Jiexin Kong
#     NetID:          jk2145
#     Version:        Python 3.7
#     Project 1:      
# ##################################################################

import requests
import pandas as pd
from pprint import pprint
import json
import csv
import sys

def main(argv):
    my_df = pd.read_csv('processed_us_zips.csv', sep=',', encoding='latin1')
    zip_list = list(my_df['zip'])
    # zip_list = zip_list[24751:]
    # print(zip_list)
    data_collect(zip_list)

    # clean data for each file
    commercial_file = 'commercial.csv'
    industrial_file = 'industrial.csv'
    residential_file = 'residential.csv'
    city_file = 'city.csv'

    data_cleanning(commercial_file)
    data_cleanning(industrial_file)
    data_cleanning(residential_file)
    data_cleanning(city_file)
    
def data_collect(zip_list):
    API_list = ['aIkM6cqxgoS0esWtN9SCOGLVitq4jzTjEZHA9b3S','kWLbVfiSMvEHQ9bmxyTFSWtjVXwVAOuedOjeh8Tr',
                'kWTyswn27xowvhPKFblBDCPDuduY77yMY2h4FVKC','tlnKZL4v3pKFuH37cYVdiS6EnThDtbWJtp1Lc0fH',
                '2Y5RfgeQNnzMJcZN5ztXQIF5itlGch6hK9csMi4J','070ZSTqYqd4s9dDlV26bxJA8D90fVyyFkSD4iyqp',
                'ii62ZSxh5AbbN6GReOaOimfwGoCrOrGW2GoC6aLU','69sZLGN6OtWVhxn7awOssaXf4QlQOIqZO63ZWpRz',
                'cz9hP2hhfhdWsInKAruMJ71CxuxMGedWMnIEAIDU','nuLTk59mnJgszS0JvlFtWZhdlggkHAN3nUehOgqX',
                'TQWSKCkLtw9115T6yBfNVvUCTGswHvts0XnhTAce','37CwKyV3b1bdJLvdqXoKepX3H8ndX5mCVogomNIN',
                'qviaUY9YKNXmlBUK5RAndY5LifbuDn9uQk1RaNNs','dgsCrcqIe0CjmOi62IkxWHcqPvxvJeUugtFLE97k',
                'AH7TSdQglkqxTXdhAAivhPHmigk93tzbjsOv7fcR','I08bJTWnghteT67ylmJoFf4MQl6GiQaPxmX4txfK',
                '2vGg501ZAng9KD9c06pJvt0J2o0BJcealDPJxeSZ','Lpfdf1Igjc1mlCzlDGaHEoICaqLTiz2ey4nciWy4',
                'lBhhKIEpbNTLZfgNpHtcD4JcMDh3S5H9mP46vdbD','n5eqwcemuyGOXOJkukyUiXW3XpW4uRffZbFt8Ruu',
                'iuTDfpv8Rcybk0dtpOZSLw5OQff8rZ6XLbtK81gM','qkUXKZMPUdrSXxfpOVb1UvH1omdlylwBTXa7Eg4j',
                't5mS3lvGRSddVvGgkh9qNI2uxqKWVY7LwxgeuBRJ','9PvcToTzOSUt2UcjKACjZCDwvMML46ysYM2EPGSR',
                'aIkM6cqxgoS0esWtN9SCOGLVitq4jzTjEZHA9b3S','kWLbVfiSMvEHQ9bmxyTFSWtjVXwVAOuedOjeh8Tr',
                'kWTyswn27xowvhPKFblBDCPDuduY77yMY2h4FVKC','tlnKZL4v3pKFuH37cYVdiS6EnThDtbWJtp1Lc0fH',
                '2Y5RfgeQNnzMJcZN5ztXQIF5itlGch6hK9csMi4J','070ZSTqYqd4s9dDlV26bxJA8D90fVyyFkSD4iyqp',
                'ii62ZSxh5AbbN6GReOaOimfwGoCrOrGW2GoC6aLU','69sZLGN6OtWVhxn7awOssaXf4QlQOIqZO63ZWpRz',
                'cz9hP2hhfhdWsInKAruMJ71CxuxMGedWMnIEAIDU','nuLTk59mnJgszS0JvlFtWZhdlggkHAN3nUehOgqX',
                'TQWSKCkLtw9115T6yBfNVvUCTGswHvts0XnhTAce','37CwKyV3b1bdJLvdqXoKepX3H8ndX5mCVogomNIN',
                ]


    with open("commercial.csv", "a") as f1, open("industrial.csv", "a") as f2, open("residential.csv", "a") as f3, open("city.csv", "a") as f4:
        # write the file headers
        csv_write1 = csv.writer(f1)
        csv_head1 = ["zip","city","commercial_electric_use_min", "commercial_electric_use_avg", "commercial_electric_use_max",
                    "commercial_electric_expenditure_min", "commercial_electric_expenditure_avg", "commercial_electric_expenditure_max",
                    "commercial_gas_use_min", "commercial_gas_use_avg", "commercial_gas_use_max",
                    "commercial_gas_expenditure_min", "commercial_gas_expenditure_avg", "commercial_gas_expenditure_max"]
        csv_write1.writerow(csv_head1)
        csv_write2 = csv.writer(f2)
        csv_head2 = ["zip", "city", "industrial_electric_use_min", "industrial_electric_use_avg", "industrial_electric_use_max",
                    "industrial_electric_expenditure_min", "industrial_electric_expenditure_avg", "industrial_electric_expenditure_max",
                    "industrial_gas_use_min", "industrial_gas_use_avg", "industrial_gas_use_max",
                    "industrial_gas_expenditure_min", "industrial_gas_expenditure_avg", "industrial_gas_expenditure_max"]
        csv_write2.writerow(csv_head2)
        csv_write3 = csv.writer(f3)
        csv_head3 = ["zip", "city", "residential_electric_use_min", "residential_electric_use_avg", "residential_electric_use_max",
                    "residential_electric_expenditure_min", "residential_electric_expenditure_avg", "residential_electric_expenditure_max",
                    "residential_gas_use_min", "residential_gas_use_avg", "residential_gas_use_max",
                    "residential_gas_expenditure_min", "residential_gas_expenditure_avg", "residential_gas_expenditure_max"]
        csv_write3.writerow(csv_head3)
        csv_write4 = csv.writer(f4)
        csv_head4 = ["zip", "city", "city_fuel_use_diesel_min", "city_fuel_use_diesel_avg", "city_fuel_use_diesel_max",
                    "city_fuel_use_gas_min", "city_fuel_use_gas_avg", "city_fuel_use_gas_max"]
        csv_write4.writerow(csv_head4)

        i = 0
        j = 0
        api = API_list[0]
        for zip in zip_list:
            zip = str(zip)
            print(str(i) + ' ' + zip)
            # deal with the zip code which the first number is 0
            if len(zip) == 4:
                zip = '0' + zip
            i+=1
            # change the API when request number is larger than 990
            if i == 990:
                i = 0
                j += 1
                api = API_list[j]
                print(api)
            # request format
            BaseURL = "https://developer.nrel.gov/api/cleap/v1/energy_cohort_data"
            URLPost = {
                'zip' : str(zip),
                'api_key' : api,
                'format' : 'JSON'
            }
            response = requests.get(BaseURL, URLPost)
            jsontxt = response.text

            # Transfer jsontxt type from String to Dictionary
            data_dict = json.loads(jsontxt)
            error_dict = data_dict.get('errors')

            # if the request succeed, write the information to the file
            # otherwise print the error message to the screen
            if error_dict != []:
                print(jsontxt)
            else:
                zip = data_dict.get('inputs').get('zip')
                result = data_dict.get('result')
                for key in result.keys():
                    # print(district)
                    result_dict = data_dict.get('result').get(key).get('similar_places').get('table')
                    commercial_electric_use_dict = result_dict.get('commercial_electric_use')

                    result1 = [str(zip), key, str(result_dict.get('commercial_electric_use').get('min')), str(result_dict.get('commercial_electric_use').get('avg')), str(result_dict.get('commercial_electric_use').get('max')),
                            str(result_dict.get('commercial_electric_expenditure').get('min')), str(result_dict.get('commercial_electric_expenditure').get('avg')), str(result_dict.get('commercial_electric_expenditure').get('max')),
                            str(result_dict.get('commercial_gas_use').get('min')), str(result_dict.get('commercial_gas_use').get('avg')), str(result_dict.get('commercial_gas_use').get('max')),
                            str(result_dict.get('commercial_gas_expenditure').get('min')), str(result_dict.get('commercial_gas_expenditure').get('avg')), str(result_dict.get('commercial_gas_expenditure').get('max'))]
                    csv_write1.writerow(result1)

                    result2 = [str(zip), key, str(result_dict.get('industrial_electric_use').get('min')), str(result_dict.get('industrial_electric_use').get('avg')), str(result_dict.get('industrial_electric_use').get('max')),
                            str(result_dict.get('industrial_electric_expenditure').get('min')), str(result_dict.get('industrial_electric_expenditure').get('avg')), str(result_dict.get('industrial_electric_expenditure').get('max')),
                            str(result_dict.get('industrial_gas_use').get('min')), str(result_dict.get('industrial_gas_use').get('avg')), str(result_dict.get('industrial_gas_use').get('max')),
                            str(result_dict.get('industrial_gas_expenditure').get('min')), str(result_dict.get('industrial_gas_expenditure').get('avg')), str(result_dict.get('industrial_gas_expenditure').get('max'))]
                    csv_write2.writerow(result2)

                    result3 = [str(zip), key, str(result_dict.get('residential_electric_use').get('min')), str(result_dict.get('residential_electric_use').get('avg')), str(result_dict.get('residential_electric_use').get('max')),
                            str(result_dict.get('residential_electric_expenditure').get('min')), str(result_dict.get('residential_electric_expenditure').get('avg')), str(result_dict.get('residential_electric_expenditure').get('max')),
                            str(result_dict.get('residential_gas_use').get('min')), str(result_dict.get('residential_gas_use').get('avg')), str(result_dict.get('residential_gas_use').get('max')),
                            str(result_dict.get('residential_gas_expenditure').get('min')), str(result_dict.get('residential_gas_expenditure').get('avg')), str(result_dict.get('residential_gas_expenditure').get('max'))]
                    csv_write3.writerow(result3)

                    result4 = [str(zip), key, str(result_dict.get('city_fuel_use_diesel').get('min')), str(result_dict.get('city_fuel_use_diesel').get('avg')), str(result_dict.get('city_fuel_use_diesel').get('max')),
                            str(result_dict.get('city_fuel_use_gas').get('min')), str(result_dict.get('city_fuel_use_gas').get('avg')), str(result_dict.get('city_fuel_use_gas').get('max'))]
                    csv_write4.writerow(result4)

        f1.close()
        f2.close()
        f3.close()
        f4.close()

def data_cleanning(filename):
    with open(filename, "r") as f:
        myDataFrame = pd.read_csv(filename , sep=',', encoding='latin1')
        # pprint(myDataFrame[:10])

        # Find the number of missing values in each column
        titles = myDataFrame.columns.values.tolist()  # Obtain the dataframe's column name
        for title in titles:
            # Count the missing values number in each column
            num = list(myDataFrame[title].isna()).count(True)
            print(title + ": " + str(num))

        # Remove rows with missing observations
        myDataFrame = myDataFrame.dropna(axis = 0, inplace = True)

        f.close()

if __name__ == "__main__":
    main(sys.argv)