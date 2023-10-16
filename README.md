# Greenhouse gas emissions
------------------------------
Data visualization for Global GHG emissions (tonnes CO2eq) by countries and by year and energy type.

# Usage
A brief guide of how to use carbon_footprint :

To run locally you need to activate the environment then run the command line as following : 
```
conda env create -f environment_footprint.yml
conda activate footprint_env
cd src/
python main.py
```

# Algorithm flow
The main script will follow this flow :

~~~
1. Parse the file data/Carbon footprint exercise.xlsx file and produce datas from the file.
2. Convert metrics to ensure the uniformity, by that it means:
    . Convert on dataframe company overview the column named Area ft2 -> m2 by following the formula : value_m2 = value_ft2 * 0.092903.
    . Convert values units comsumption data to kWh by following this formula :
        . Gallons - Diesel (kWh) : (x /0.264172) * 10
        . Gallons - Gaz (kWh) : kwh_gas = (x /0.264172) * 0.0088
        . Gallons - Propane (kWh) : (x /0.264172) * 9.1
        . Liters - Diesel (kWh) : x * 10
        . Liters - Gaz (kWh) : x * 0.0088
        . Liters - Propane (kWh) : x * 9.1
        . Emission factors fuel (MMBTU to kWh): x * 293.07107
        . Emission factors Electricity (mWh -> kWh):
            . Electricity = x * 1000
3. Calculate GHG emissions :
    . Convert kCo2 to tCo2 by using 1 kg -> 0.001 Tonnes.
    . Convert gCo2 to tCo2 by using 1 gCO2eq/kWh = 1 ton of CO2eq/GWh -> 1000 (0.001*1000000) KgCO2eq/kWh = 1 ton of CO2eq/Kwh
    . Calculate with this formula: Total GHG emissions (tCO2eq) = Energy consumption * Emission factors * Global Warming Potential (GWP)
4. Normalize GHG emissions :
    . Normalization by using z score = (x - mean) / standard_deviation
5. Display results as interactive plots in html and png plots files in the directory `results/`.
6. Save transformations data on results/data_results.xlsx
~~~

# Output
The output will be display in results folder with two figures GHG emissions based on country and on year/energy type and two html representing the interactive figures.
##### Total GHG emissions (tonnes CO2eq) per countries:
![GHG per country](results/ghg_country.png)

<b>Interpretation : </b>
The percentage represent total GHG emissions per country.

##### Total normalized GHG emissions (tonnes CO2eq) per year and energy type:
![GHG per year per energy type](results/ghg_year_energy.png)

<b>Interpretation : </b>
The value tells how many standard deviations is away from the mean. If a value is equal to 0, it is on the mean. A positive value indicates the raw score is higher than the mean average. Negative value represents below the mean average.
# Copyright
Yasmine Draceni - October 2023


