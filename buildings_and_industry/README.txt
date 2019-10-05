This is the README.txt for buildings_and_industry folder structure.

Folder Structure:
../buildings_and_industry/
	/clean_data_py/
		# Contains all data cleaning python files in this folder.
		# If open files, the PATH is incorrect, please correct the file path
		# Some CSV or JSON file is too big, the zip files are provided
		# Please unzip all zipped files when you start the test
			
		# Clean building_stock_summaries.csv in folder - /data_in_csv/
		# Remove all mising values, because the building count is missing
		# All other dynamic values will be missing
		# That means if missing values, building count must be missing
		# If building count is missing, the row is not valuable to analyze
		# Replace unclear data with clear data
		# Replace sector to full words
		# Data is all cleaned in folder - /cleaned_data_csv/
		/clean_building_stock_summaries_data.py

		# This is the cleaned py file to clean main data for this project
		# Clean commercial_building.csv in folder - /data_in_csv/
		# That contains eletricity and natural gas usages in commercial buildings
		# Some missing values are allowed, please check the report to get more details
		# Data is all cleaned in folder - /cleaned_data_csv/
		/clean_commercial_building_data.py

		# This is the cleaned py file to clean main data for this project
		# Clean industrial.csv in folder - /data_in_csv/
		# That contains eletricity and natural gas usages in commercial buildings
		# Some missing values are allowed, please check the report to get more details
		# Data is all cleaned in folder - /cleaned_data_csv/
		/clean_industril_data.py

	/cleaned_data_csv/
		# Contains all cleaned data in CSV files
		# Some CSV or JSON file is too big, the zip files are provided
		# Please unzip all zipped files when you start the test

		# That zip file contains cleaned_building_stock_summaries_data.csv
		# Please unzip it before the test is started
		# This contains CSV file for cleaned data of building stock summaries
		# This is a extra more data set, not main data set
		# It supports the analysis of buildings and industrials
		/cleaned_building_stock_summaries_data_csv.zip

		# That zip file contains /cleaned_commercial_building.csv
		# Please unzip it before the test is started
		# This contains CSV file for cleaned data of commercial buildings
		# And situations of using of electricity and natural gas
		# This is the main data set for the project
		/cleaned_commercial_building_csv.zip

		# This is the CSV file for cleaned data of industrials
		# And situations of using of electricity and natural gas
		# This is the main data set for the project
		/cleaned_industrial_data.csv

	/collect_data_py/
		# This folder contains all py files that collect data from data.gov
		# All original data are exported to folder - /data_in_json/ in JSON files

		# Collect commercial buildings and industrials
		# This contains locations and usages of electricty and natural gas
		# This collect the main data for this project
		/collect_building_and_industrial_data.py

		# Collect the disclosures of commercial buildings
		# The data is not main data, it is a extra one data
		/collect_building_disclosures_data.py

		# Collect the stock summaries of commercial buildings
		# The data is not main data, it is a extra one data
		/collect_building_stock_summaries_data.py

		# Collect the limitation of housing units
		# The data is not main data, it is a extra one data
		/collect_lmi_housing_units_data.py

		# Collect the solar photovoltaics of small buildings
		# The data is not main data, it is a extra one data
		/collect_small_building_pv_data.py

	/data_in_csv/
		# Convert original JSON data to not-clean data in CSV
		# Remove some NOT FOUND JSON data
		# Wrang JSON to dataframe structure
		# Some data are not good JSON, reomove them
		
		# The data of building disclosure
		# It is not main data set
		/building_disclosure.csv

		# The data of building stock summaries
		# This is a zip file that contains building_stock_summaries.csv
		# Since the CSV file is too big to upload
		# Please unzip it when the test is started
		# It is not main data set
		/building_stock_summaries_csv.zip

		# The data of commercial buildings
		# And the usages of electricity and natural gas
		# This is a zip file that contains commercial_building.csv
		# Since the CSV file is too big to upload
		# Please unzip it when the test is started
		# It is the main data set
		/commercial_building_csv.zip

		# The data of industrial
		# And the usages of electricity and natural gas
		# It is the main data set
		/industrial.csv

		# The data of the limitation of housing units
		# It is not main data set
		/lmi_housing_units.csv

		# The data of the solar photovoltaics of small building
		# It is not main data set
		/small_building_pv.csv

	/data_in_json/
		# This folder contains all JSON data from the energy of data.gov
		# They are all original data
		# If some files are zip, please unzip them first

		# Main data set
		/activities_commercial_json.zip
		/activities_industrial_json.zip

		# Supporting data set, not main data set
		/building_disclosure.json
		/building_stock_summaries_json.zip
		/lmi_housing_units.json
		/small_building_pv.json

	/process_data_py/
		# Convert JSON to dataframe
		# Recognize JSON and correc formation
		# Remove broken JSON
		# Remove NOT FOUND DATA
		# Recoganize JSON to corressponding attributes and values

		/process_buidling_disclosures_data.py
		/process_building_stock_summaries_data.py
		/process_commercial_building_data.py
		/process_industrial_data.py
		/process_lmi_housing_units_data.py
		/process_small_building_pv.py




Info Backup: 
For buildings and industrials data, there are two classifications: commercial buildings and industrials. These data are necessary for this project because the goal of this project is to obtain a detailed view of how energy consumption occurs in different Industry Classification System of North America. There are 18 attributes in both commercial buildings data and industrials data:
1.	city: the city name of USA
2.	state_abbr: the state of USA 
3.	zip: the zip of USA
4.	type: the type of user – commercial building or industrial
5.	town: Small towns under the city
6.	naics_3: the code of North American Industry Classification System – Third Class
7.	electricity_users: Different kinds of business under NAICS 3 who use electricity
8.	number_of_electricity_establishments: the number of business who uses electricity
9.	electricity_use: the total used amount of electricity
10.	rank_of_electricity_use: the rank of use-electricity amount in this city
11.	electricity_use_per_establishment: the average electricity amount 
12.	rank_of_electricity_use_per_establishment: the rank of average electricity amount in this state
13.	natural_gas_users: Different kinds of business under NAICS 3 who use natural gas
14.	number_of_natural_gas_establishments: the number of business who uses natural gas
15.	natural_gas_use: the total used amount of natural gas
16.	rank_of_natural_gas_use: the rank of use-natural-gas amount in this city
17.	natural_gas_use_per_establishment: the average natural gas amount
18.	rank_of_natural_gas_use_per_establishment: the rank of average natural gas amount in this state
Therefore, the data could produce many statistics and locate some cities where energy consumption is higher than others. There might be ought to strengthen measurements of saving energy. Besides, the data can help people to predict the potential cities with high energy consumption and take measures to save energy. To predict, there should be more historic data to collect in different years to analyze the change tendency.

Collecting New Data:
The original data of commercial buildings and industrials are stored in the data_in_json folder. The files all contain original JSON data from data.gov. The JSON files are processed to CSV files in the data_in_csv folder. The files industrial.csv and commercial_building.csv contain main data of this analysis project, and other data will support the project with the necessary operation.

Data Cleaning
The data also did the second procession and cleaning with solving missing values, converting correct formation, removing unclear values, and so on. The cleaned data are located in the folder – cleaned_data_csv. The README.txt is provided to show the details of the structure of the data location and folder branches. Please check README.txt to get more details about folder structure and file locations.



Data Cleanliness
The fractions of missing values in cleaned data are: 
Commercial building:
city                                         0.000000
state_abbr                                   0.000000
zip                                          0.000000
type                                         0.000000
town                                         0.000000
naics_3                                      0.000000
electricity_users                            0.000000
number_of_electricity_establishments         0.000000
electricity_use                              0.000000
rank_of_electricity_use                      0.000000
electricity_use_per_establishment            0.001052
rank_of_electricity_use_per_establishment    0.000000
natural_gas_users                            0.000000
number_of_natural_gas_establishments         0.000000
natural_gas_use                              0.118833
rank_of_natural_gas_use                      0.000000
natural_gas_use_per_establishment            0.118952
rank_of_natural_gas_use_per_establishment    0.000000

Industrial:
city                                         0.000000                                                                   
state_abbr                                   0.000000                                                                   
zip                                          0.000000                                                                   
type                                         0.000000                                                                   
town                                         0.000000                                                                   
naics_3                                      0.000000                                                                   
electricity_users                            0.000000                                                                   
number_of_electricity_establishments         0.000000                                                                   
electricity_use                              0.000000                                                                   
rank_of_electricity_use                      0.000000                                                                   
electricity_use_per_establishment            0.004456                                                                   
rank_of_electricity_use_per_establishment    0.000000                                                                   
natural_gas_users                            0.000000                                                                   
number_of_natural_gas_establishments         0.000000                                                                   
natural_gas_use                              0.000000                                                                   
rank_of_natural_gas_use                      0.000000                                                                   
natural_gas_use_per_establishment            0.003121                                                                   
rank_of_natural_gas_use_per_establishment    0.000000

Since some businesses only use either natural gas or electricity, their data of the corresponding attribute will be missing. The missing values are allowed. Therefore, the commercial buildings and industrials data are enough cleaned for analysis in this project. For other data, they are supporting the project when it analyzes the commercial buildings and industrials data. They will be processed when the project needs them. They are extra more data.



















