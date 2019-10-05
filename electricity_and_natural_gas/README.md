#README
---

# CollectData.py

This is a python script to collect data from Developer Network and clean the data. There are some limitations about this website. 

Firstly, the rate limit of API is 1000 requests per hour. And there are about 33,000 zip codes to request. So we need at least 33 APIs to request iteratively.

Secondly, the request will be blocked or failed when the zip code is 70085, 70091 or 72801. So I use a if conditional statement to ignore them.

Thirdly, there are 67731 results which are more than the amount of zip codes (32969). Because there might be more than 1 city attached to the same zip code. 

# API.txt

There are 33 APIs in this file.

# processed_us_zips.csv

There are all zip codes of the United States. Because csv file ignore the beginning 0 of numbers, the beginning zip codes are 4 in length rather than 5. So before requesting with it, it should be transfered firstly.

# output.txt

The statistic results - fractions of missing values or incorrect values (noise) are stored in this file.

# residential.csv

The collected data about residential electricity and natural gas consumptions are stored in this file.

# commercial.csv

The collected data about commercial electricity and natural gas consumptions are stored in this file.

# industrial.csv

The collected data about industrial electricity and natural gas consumptions are stored in this file.

# electricity_and_natural_gas.csv

Extract some attributes (except the minimum and maximum values) to store in this file.

# cleaned_residential.csv

The cleaned data about residential electricity and natural gas consumptions are stored in this file.

# cleaned_commercial.csv

The cleaned data about commercial electricity and natural gas consumptions are stored in this file.

# cleaned_industrial.csv

The cleaned data about industrial electricity and natural gas consumptions are stored in this file.

# cleaned_electricity_and_natural_gas.csv

The cleaned merged attributes about electricity and natural gas consumptions are stored in this file.

## Meanings of each column

* [housing_units](https://www.census.gov/housing/hvs/definitions.pdf)

    A housing unit is a house, an apartment, a group of rooms, or a single room occupied or intended for occupancy as separate living quarters.

* total_pop

    Total population of USA.

* num_establishments

    The number of commercial establishments (in commercial.csv). 
    The number of industrial establishments (in industrial.csv).

* elec_1kdollars

    The expenditures of electricity, and the unit is 1k dollars.

* elec_mwh

    The usage of electricity, and the unit is megawatt hour.

* gas_1kdollars

    The expenditures of natural gas, and the unit is 1k dollars.

* gas_mcf

    The usage of natural gas, and the unit is 1 thousand cube feet.

* elec_1kdollars_bin_min

    The minimum value of bins for elec_1kdollars.

* elec_1kdollars_bin_max

    The maximum value of bins for elec_1kdollars.

* elec_mwh_bin_min

    The minimum value of bins for elec_mwh.

* elec_mwh_bin_max

    The maximum value of bins for elec_mwh.

* gas_1kdollars_bin_min

    The minimum value of bins for gas_1kdollars.

* gas_1kdollars_bin_max

    The maximum value of bins for gas_1kdollars.

* gas_mcf_bin_min

    The minimum value of bins for gas_mcf.

* gas_mcf_bin_max

    The maximum value of bins for gas_mcf.

* elec_lb_ghg

    How much greenhouse gas is produced per megawatt hour electricity?

* elec_min_lb_ghg

    The minimum value of bins for elec_lb_ghg.

* elec_max_lb_ghg

    The maximum value of bins for elec_lb_ghg.

* gas_lb_ghg

    How much greenhouse gas is produced per thousand cube feet gas?

* gas_min_lb_ghg

    The minimum value of bins for gas_lb_ghg.

* gas_max_lb_ghg

    The maximum value of bins for gas_lb_ghg.

