

import pandas as pd
import numpy as np

data = pd.read_csv("C:/Users/nlowe\Downloads/aircraft_accidents in oceans_unknown - aircraft_accidents.csv")
num_accidents = data.shape[0] # saving the count of total accidents
data.head()

print(data)

nulls_count_precentage={ col_name : (data[col_name].isna().sum(),
                                str( round( 100 * data[col_name].isna().sum() / data.shape[0] ,2))+" %")
                                for col_name in data.columns}
print(nulls_count_precentage)

data.nunique()

iso_map = {country: get_country_code(country) for country in data["Country"].unique()}
