
#import Packages
import pandas as pd
import numpy as np
import datetime as dt
import pycountry
import plotly.express as px
import matplotlib

#import Data sets
data = pd.read_csv(r"C:\Users\nlowe\Downloads\aviation_accidents in countries - aviation_accidents.csv")
# saving the count of total accidents
num_accidents = data.shape[0]
data.head()

print(data)

#How many null values are there within the data
nulls_count_precentage={ col_name : (data[col_name].isna().sum(),
                                str( round( 100 * data[col_name].isna().sum() / data.shape[0] ,2))+" %")
                                for col_name in data.columns}
print(nulls_count_precentage)

#How many unique values are there within the data
data.nunique()

#create a function to identify country code for each country
def get_country_code(country):
    try:
        result = pycountry.countries.search_fuzzy(country)
    except:
        return np.nan
    else:
        return result[0].alpha_3
iso_map = {country: get_country_code(country) for country in data["Country"].unique()}

# ammending the Dataframe - top 15 country and combine all other countries in 'other'
data["country_code"] = data["Country"].map(iso_map)

countries_df = data.groupby(['Country','country_code']).size().sort_values(ascending=[False])\
         .to_frame().reset_index()\
        .rename(columns= {0: 'count_accidents'})

countries_df_part=countries_df[:15]
accidents_other = countries_df['count_accidents'][15:].sum()
df2 = pd.DataFrame([['other','other', accidents_other]], columns=['Country','country_code','count_accidents'])
countries_df_part=countries_df_part.append(df2)


#Create pie chart detaling only the top 15 countries, grouping whats left ito 'other'
fig = px.pie(countries_df_part,
            values='count_accidents',
            names='Country',
            title='15 countries where the most accidents happend')
fig.update_traces( textinfo='value+label',textfont_size=10)
fig.show()

#Create a global view (scatter chart) of the number of accidents by country
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

# Fixing the category column and data
# Some null values exist in the in the category column,
# Drop Null values in the category column
categories_filtered=data.dropna(subset=['category'])

# Creating 2 functions to split Cause and Result data and label, adding 2 columns about the accident cause and result
def cause_accident(value):
    if value.find('A')>=0:
        return 'Accident'
    if value.find('I')>=0:
        return 'Incident'
    if value.find('H')>=0:
        return 'Hijacking'
    if value.find('C')>=0:
        return 'Criminal occurrence'
    if value.find('O')>=0:
        return 'Other occurrence'
    if value.find('U')>=0:
        return 'Unknown'

def result_accident(value):
    if value.find('1')>=0:
        return 'Hull Loss'
    if value.find('2')>=0:
        return 'Repairable Damage'


# Adding 2 columns representing the cause and result of the data individually
causes = categories_filtered['category'].map(cause_accident)
results = categories_filtered['category'].map(result_accident)
categories_filtered = pd.concat([categories_filtered, causes, results], axis=1, join="inner")
categories_filtered.columns = ['Country', 'date', 'Air-craft type', 'registration name/mark',
       'operator', 'fatilites', 'location', 'category', 'country_code',
       'Accident_cause', 'Accident_result']

# Finding the pair of result-cause combination
result_cause = categories_filtered.groupby(
                                ['Accident_cause','Accident_result'])  \
                                .size().sort_values(ascending=False).  \
                                to_frame().reset_index().  \
                                rename(columns={0: 'count_accidents'})

# the accident where the result = hull loss
hull_loss_df = result_cause[result_cause['Accident_result']=='Hull Loss']
# the accident where the result = Repairable Damage
repairable_df = result_cause[result_cause['Accident_result']=='Repairable Damage']
#
result_by_cause_df = pd.merge(hull_loss_df, repairable_df, how='outer', on = 'Accident_cause').fillna(0)
result_by_cause_df[:2]

# Create a list for visualisation
list_draw= [result_by_cause_df["count_accidents_x"].to_list()\
         ,result_by_cause_df["count_accidents_y"].to_list()]

print(list_draw)

fig = px.imshow(list_draw,
                labels=dict(x="Cause of Accident", y="Result of Accident", color="Accidents"),
                x= result_by_cause_df["Accident_cause"],
                y=["Hull Loss","Repairable Damage"],
                text_auto = True
               )
fig.update_xaxes(side="top" )
fig.show()