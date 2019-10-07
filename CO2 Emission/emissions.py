# ##################################################################
#     Author:         Jiexin Kong
#     NetID:          jk2145
#     Version:        Python 3.7
#     Project 1:      
# ##################################################################

import requests
import pandas as pd
import numpy as np
from pprint import pprint
import json
import csv
import sys

def main(argv):
    my_df = pd.read_csv('processed_us_zips.csv', sep=',', encoding='latin1')
    DataFrame = my_df.drop_duplicates(['state_id']) 
    abbr_list  = np.array(DataFrame['state_id']).tolist()
    # print(abbr_list)
    # data_collect(abbr_list)

    data_cleanning("emission.csv")
    

def data_collect(abbr_list):
    type_list = ['commercial', 'electric', 'residential', 'industrial', 'transportation', 'total']
    
    with open("emission.csv", "w") as f:
        csv_write = csv.writer(f)
        csv_head = ['state_abbr','type','series_id', 'name', 'units', 'f', 'unitsshort', 'description', 'copyright', 'source', 'iso3166', 'geography',
                      'start', 'end', 'updated', '1980', '1981', '1982','1983','1984','1985', '1986', '1987', '1988', '1989', '1990',
                      '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
                      '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']
        csv_write.writerow(csv_head)

        for state in abbr_list:
            print(state)
            for rType in type_list:
                print(rType)
                BaseURL = "https://developer.nrel.gov/api/cleap/v1/state_co2_emissions"
                URLPost = {
                    'state_abbr' : state,
                    'type' : rType,
                    'api_key' : '2Y5RfgeQNnzMJcZN5ztXQIF5itlGch6hK9csMi4J',
                    'format' : 'JSON'
                }
                response = requests.get(BaseURL, URLPost)
                jsontxt = response.text

                # print(jsontxt)
                # Transfer jsontxt type from String to Dictionary
                data_dict = json.loads(jsontxt)
                error_dict = data_dict.get('errors')

                # if the request succeed, write the information to the file
                # otherwise print the error message to the screen
                if error_dict != []:
                    print(jsontxt)
                else:
                    result_dict = data_dict.get('result')
                    data = result_dict[0].get('data')
                    result = [state, rType]
                    result = [state, rType, result_dict[0].get('series_id'), result_dict[0].get('name'), result_dict[0].get('units'), result_dict[0].get('f'),
                              result_dict[0].get('unitsshort'), result_dict[0].get('description'), result_dict[0].get('copyright'), result_dict[0].get('source'),
                              result_dict[0].get('iso3166'), result_dict[0].get('geography'), str(result_dict[0].get('start')), str(result_dict[0].get('end')),result_dict[0].get('updated'),
                              str(data.get('1980')), str(data.get('1981')), str(data.get('1982')), str(data.get('1983')), str(data.get('1984')), str(data.get('1985')), str(data.get('1986')),
                              str(data.get('1987')), str(data.get('1988')), str(data.get('1989')), str(data.get('1990')), str(data.get('1991')), str(data.get('1992')), str(data.get('1993')),
                              str(data.get('1994')), str(data.get('1995')), str(data.get('1996')), str(data.get('1997')), str(data.get('1998')), str(data.get('1999')), str(data.get('2000')),
                              str(data.get('2001')), str(data.get('2002')), str(data.get('2003')), str(data.get('2004')), str(data.get('2005')), str(data.get('2006')), str(data.get('2007')), 
                              str(data.get('2008')), str(data.get('2009')), str(data.get('2010')), str(data.get('2011')), str(data.get('2012')), str(data.get('2013')), str(data.get('2014')),
                              str(data.get('2015')), str(data.get('2016'))]
                    csv_write.writerow(result)
                    
        f.close()

def data_cleanning(filename):
    output = open('output1.txt', 'a')
    print(filename)
    with open(filename, "r") as f:
        myDataFrame = pd.read_csv(filename , sep=',', encoding='latin1')
        deleteColumn(myDataFrame, output)
        findMiss(myDataFrame, output)
        findInvaild(myDataFrame, output)
        myDataFrame.to_csv("Clean_" + filename, index = False)
        f.close()
    output.close()

def findMiss(myDataFrame, output):
    output.write("Find the fraction of missing values in each column:"+'\n')
    # Find the number of missing values in each column
    titles = myDataFrame.columns.values.tolist()  # Obtain the dataframe's column name
    for title in titles:
        # Count the missing values number in each column
        num = list(myDataFrame[title].isna()).count(True)
        # print(title + ": " + str(num * 1.00 / len(myDataFrame)))
        output.write(title + ": " + str(num * 1.00 / len(myDataFrame))+'\n')

    # Remove rows with missing observations
    myDataFrame = myDataFrame.dropna(axis = 0, inplace = True)
    output.write('\n')

def deleteColumn(myDataFrame, output):
    output.write("Delete the duplicate content column:" + '\n')
    output.write("The column of the dataframe is:" + str(myDataFrame.shape[1])+ '\n')
    output.write("The rows of the dataframe is:" + str(myDataFrame.shape[0])+ '\n')
    delete(myDataFrame, output, "units")
    delete(myDataFrame, output, "f")
    delete(myDataFrame, output, "unitsshort")
    delete(myDataFrame, output, "description")
    delete(myDataFrame, output, "copyright")
    delete(myDataFrame, output, "source")
    delete(myDataFrame, output, "start")
    delete(myDataFrame, output, "end")
    delete(myDataFrame, output, "updated")
    myDataFrame.drop(["iso3166"],axis=1,inplace=True)
    myDataFrame.drop(["geography"],axis=1,inplace=True)
    output.write("Now The column of the dataframe is:" + str(myDataFrame.shape[1])+ '\n')
    output.write('\n')

def delete(myDataFrame, output, column):
    output.write("The duplicate content number of " + column +  " row is " + str(myDataFrame[column].value_counts()) + '\n')
    myDataFrame.drop([column],axis=1,inplace=True)

def findInvaild(myDataFrame, output):
    output.write("Find the fraction of invalid values in each column:"+'\n')
    titles = myDataFrame.columns.values.tolist()  # Obtain the dataframe's column name
    i = 0
    for title in titles:
        if i > 4:
            output.write(title + ": "+ str(len(myDataFrame[myDataFrame[title] < 0]) * 1.00 / len(myDataFrame))+'\n')
        i+=1
    output.write('\n')


if __name__ == "__main__":
    main(sys.argv)