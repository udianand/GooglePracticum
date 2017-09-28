import pandas as pd

############ FUNCTIONS ##############
def cal_weight(input_df, total_value):
    return input_df["Value"].sum()/total_value

def mapping_county_to_region(county_name):
    return county_production_df[county_production_df['County'] == county_names.upper()]["Ag District"]
############### MAIN #################

# Files
path = 'C:\\Users\Joonha Yoon\Desktop'

county_name_file = "/County_Names_IL.csv"
county_production_df = pd.read_csv(path + county_name_file)

price_file = "/IL_Corn_Price_data_Monthly.csv"
price_df = pd.read_csv(path + price_file)

weather_file = "/weather_data_example.csv"
weather_df = pd.read_csv(path + weather_file)

# Weighted Average.
region_names = county_production_df["Ag District"].drop_duplicates()
region_df = pd.DataFrame(0, index=region_names, columns=["Weight"])
grouped_df = county_production_df.groupby(["Ag District"])

total_production = county_production_df["Value"].sum()
for i in region_names:
    print(grouped_df.get_group(i))
    region_df.loc[i] = cal_weight(grouped_df.get_group(i), total_production)

###### Mapping county to region ######

county_region_df = pd.DataFrame(0, index=county_production_df["County"].drop_duplicates(), columns="Ag District")

for county_names in weather_df["COUNTY"]:
    print(mapping_county_to_region(county_names))

