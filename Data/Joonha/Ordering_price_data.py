import pandas as pd

path = ""

ordered_price_data = pd.DataFrame(index = price_data.index, columns = price_data.columns)
row_index = 0;
price_data_yearly_grouped = price_data.groupby("Year")
for years in price_data["Year"].drop_duplicates():
    temp_df = price_data_yearly_grouped.get_group(years)
    for i in range(len(temp_df)):
        ordered_price_data.iloc[row_index] = temp_df.iloc[len(temp_df)-1-i]
        row_index += 1

ordered_price_data.to_csv(path + '/IL_Corn_Price.csv')

