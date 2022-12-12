

import pandas as pd
import numpy as np
import datetime as dt
import pycountry
import plotly.express as px

data = pd.read_csv(r"C:\Users\nlowe\Downloads\aviation_accidents in countries - aviation_accidents.csv")
num_accidents = data.shape[0] # saving the count of total accidents
data.head()

print(data)

nulls_count_precentage={ col_name : (data[col_name].isna().sum(),
                                str( round( 100 * data[col_name].isna().sum() / data.shape[0] ,2))+" %")
                                for col_name in data.columns}
print(nulls_count_precentage)

data.nunique()
def get_country_code(country):
    try:
        result = pycountry.countries.search_fuzzy(country)
    except:
        return np.nan
    else:
        return result[0].alpha_3
iso_map = {country: get_country_code(country) for country in data["Country"].unique()}

data["country_code"] = data["Country"].map(iso_map)

countries_df = data.groupby(['Country','country_code']).size().sort_values(ascending=[False])\
         .to_frame().reset_index()\
        .rename(columns= {0: 'count_accidents'})

countries_df_part=countries_df[:15]
accidents_other = countries_df['count_accidents'][15:].sum()
df2 = pd.DataFrame([['other','other', accidents_other]], columns=['Country','country_code','count_accidents'])
countries_df_part=countries_df_part.append(df2)

fig = px.pie(countries_df_part,
            values='count_accidents',
            names='Country',
            title='15 countries where the most accidents happend')
fig.update_traces( textinfo='value+label',textfont_size=10)
fig.show()

fig = px.scatter_geo(countries_df, locations="country_code",
                     color="Country", # which column to use to set the color of markers
                     hover_name="Country", # column added to hover information
                     size="count_accidents", # size of markers
                     projection="natural earth")
fig.show()

countries_operators_df = data.groupby(['Country','country_code','operator']).size().sort_values(ascending=[False])\
    .to_frame().reset_index()\
    .rename(columns= {0: 'count_accidents'})
fig = px.treemap(countries_operators_df, path=[px.Constant('world'), 'Country', 'operator'], values='count_accidents',
                   hover_data=['country_code'])
fig.update_traces(root_color="lightgrey")
fig.show()

