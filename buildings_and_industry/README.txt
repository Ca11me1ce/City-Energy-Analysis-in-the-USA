This is the README.txt for buildings_and_industry follder.

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

















