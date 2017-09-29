# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:26:56 2017

@author: Joonha Yoon
"""

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams


############ FUNCTIONS ##############
def mapping_county_to_region(county_name):
    return county_production_df[county_production_df['County'] == county_names.upper()]["Ag District"]

def edit_price_df(price_data):
    ordered_price_data = pd.DataFrame(index = price_data.index, columns = price_data.columns)
    row_index = 0;
    price_data_yearly_grouped = price_data.groupby("Year")
    for years in price_data["Year"].drop_duplicates():
        temp_df = price_data_yearly_grouped.get_group(years)
        for i in range(len(temp_df)):
            ordered_price_data.iloc[row_index] = temp_df.iloc[len(temp_df)-1-i]
            row_index += 1

    #ordered_price_data.to_csv(path + '/IL_Corn_Price.csv')
    return ordered_price_data

############### MAIN #################
# Files
path = 'C:\\Users\Joonha Yoon\Desktop\Week_4'

county_name_file = "/County_Names_IL.csv"
county_production_df = pd.read_csv(path + county_name_file)

price_file = "/IL_Corn_Price_data_Monthly.csv"
price_df = pd.read_csv(path + price_file)

weather_file = "/weather_data_example.csv"
weather_df = pd.read_csv(path + weather_file)

# Weighted Average.
region_names = county_production_df["Ag District"].drop_duplicates()
grouped_df = county_production_df.groupby(["Ag District"])
weather_group_df = weather_df.groupby(["COUNTY"])
total_production = county_production_df["Value"].sum()
county_weight_df = pd.DataFrame(index=county_production_df["County"].drop_duplicates(), columns=["Weight"])

for i in region_names:
    print(grouped_df.get_group(i))

for county in county_weight_df.index:
    county_weight_df.loc[county] = (county_production_df[county_production_df["County"] == county]["Value"] / total_production).iloc[0]

for county in county_production_df["County"]:
    weather_group_df.get_group(county.lower())

for county in weather_df["COUNTY"]:
    weather_group_df.get_group(county.lower())

year_month_columns = weather_group_df.get_group(weather_df["COUNTY"].iloc[0])[["YEAR", "MONTH"]]
averaged_weather_data = pd.DataFrame(0, index = range(len(year_month_columns)), columns = weather_df.columns[4:])

for county in weather_df["COUNTY"].drop_duplicates():
    averaged_weather_data += weather_group_df.get_group(county)[weather_df.columns[4:]] * county_weight_df.loc[county].iloc[0]



#######################Price data analysis#####################################
price_data = edit_price_df(price_df)
date_list = []
for i in range(len(price_data)):
    date_list.append(pd.to_datetime((str(price_data["Year"].iloc[i]) +"-"+ price_data["Period"].iloc[i]), infer_datetime_format=True).date())

price_processed = pd.DataFrame(data = price_data["Value"].values, columns = ["Value"])

for i in range(len(date_list)):
  date_list[i] = pd.Timestamp(date_list[i])

price_processed.index = date_list

decomposition = seasonal_decompose(price_processed, freq = 30)  # monthly

price_trend = decomposition.trend
price_seasonal = decomposition.seasonal
price_residual = decomposition.resid

plt.subplot(411)
plt.plot(price_processed, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(price_trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(price_seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(price_residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

