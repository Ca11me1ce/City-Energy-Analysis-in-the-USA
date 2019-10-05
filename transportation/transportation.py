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
    zip_list = zip_list[27092:]
    # print(zip_list)
    data_collect(zip_list)

    transportation_file = 'transportation.csv'
    data_cleaning(transportation_file)

def data_collect(zip_list):
    API_list = ['qviaUY9YKNXmlBUK5RAndY5LifbuDn9uQk1RaNNs','dgsCrcqIe0CjmOi62IkxWHcqPvxvJeUugtFLE97k',
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

    with open("transportation.csv", "a") as f:
        csv_write = csv.writer(f)
        csv_head = ["zip","city","city_vmt_estimate", "natl_avg_vmt_estimate", "natl_per_capita_vmt_estimate"]
        # csv_write.writerow(csv_head)

        i = 0
        j = 0
        api = API_list[0]
        #for zip in [20007]:
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
            BaseURL = "https://developer.nrel.gov/api/cleap/v1/city_vmt_estimates"
            URLPost = {
                'zip' : zip,
                'api_key' : api,
                'format' : 'JSON'
            }
            response = requests.get(BaseURL, URLPost)
            jsontxt = response.text

            # Transfer jsontxt type from String to Dictionary
            data_dict = json.loads(jsontxt)
            error_dict = data_dict.get('errors')

            if error_dict != []:
                print(jsontxt)
            else:
                result = data_dict.get('result')
                for key in result.keys():
                    result_dict = data_dict.get('result').get(key)
                    result = [zip, key, str(result_dict.get('city_vmt_estimate')), str(result_dict.get('natl_avg_vmt_estimate')),
                              str(result_dict.get('natl_per_capita_vmt_estimate'))]
                    csv_write.writerow(result)
        f.close()

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
