## emission.py
This is a python script file to collect and clean data.
For collecting data, it gathers data from Developer Network. The request is based on the state abbreviation. 
For cleaning data part, this data set has none missing value and invalid value(which numbers value is smaller than 0). However, some columns of this data set are quite duplicated. To keep data set concise and clean, I delete all repeated items.

## emission.csv
This file is stored the data collected from the Developer Network, which has 306 rows.

## Clean_emission.csv
This file is stored the data which be processed.

## output1.txt
This file records the cleanning process.

## Main data attributes and description
# type: 
Resource type, such as industrial, commercial, residential, electric, transportation, total
# series_id: 
The identifier of the record
# name: 
The textual representation of the record
# Data from 1980 to 2016: 
The specific data of carbon dioxide emission from 1980 to 2016
