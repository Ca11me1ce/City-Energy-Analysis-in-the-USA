# energy.py
This is a python script file to collect and clean data.
For collecting data, it gathers data from Developer Network. The request is based on the zip code. Since the website API limitation is 1000 per hour, I request 24 API to request data. 
For cleaning data part, this data set has none missing value and invalid value(which numbers value is smaller than 0). 

# industrial.csv
This file is stored the data collected from the Developer Network, which has 67730 rows.

# commercial.csv
This file is stored the data collected from the Developer Network, which has 67730 rows.

# residential.csv
This file is stored the data collected from the Developer Network, which has 67730 rows.

# city.csv
This file is stored the data collected from the Developer Network, which has 67730 rows.

# Clean_industrial.csv
This file is stored the data which be processed.

# Clean_commercial.csv
This file is stored the data which be processed.

# Clean_residential.csv
This file is stored the data which be processed.

# Clean_city.csv
This file is stored the data which be processed.

# output.txt
This file records the cleanning process.

# Main data attributes and description
## zip: 
Zipcode for inquiry
## city: 
City name
## commercial_electric_use(min/avg/max): 
The minimize/average/maximum value of commercial electric usage
## commercial_electric_expenditure(min/avg/max): 
The minimize/average/maximum value of commercial electric expenditure
## commercial_gas_use(min/avg/max): 
The minimize/average/maximum value of commercial gas usage
## commercial_gas_expenditure(min/avg/max):	
The minimize/average/maximum value of commercial gas expenditure
## industrial_electric_use(min/avg/max)	: 
The minimize/average/maximum value of industrial electric usage
## industrial_electric_expenditure(min/avg/max): 
The minimize/average/maximum value of industrial electric expenditure
## industrial_gas_use(min/avg/max): 
The minimize/average/maximum value of industrial gas usage
## industrial_gas_expenditure(min/avg/max): 
The minimize/average/maximum value of industrial gas expenditure
## residential_electric_use(min/avg/max):
The minimize/average/maximum value of residential electric usage
## residential_electric_expenditure(min/avg/max): 
The minimize/average/maximum value of residential electric expenditure
## residential_gas_use(min/avg/max): 
The minimize/average/maximum value of residential gas usage
## residential_gas_expenditure(min/avg/max): 
The minimize/average/maximum value of residential gas expenditure
## city_fuel_use_diesel(min/avg/max): 
The minimize/average/maximum value of city diesel usage
## city_fuel_use_gas(min/avg/max): 
The minimize/average/maximum value of city gas usage


