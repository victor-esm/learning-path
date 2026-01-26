import  folium
import pandas as pd

# data downloaded from IBGE: TODO download directly from the website
df = pd.read_csv('tabela6835.csv', sep=';', skiprows=3, decimal=',', nrows=28)

# correct the row index
df.reset_index(inplace=True)
# remove unnecessary columns
df.drop(columns=['index', 'Nível', '2017', '2018'], inplace=True)
# remove unnecessary rows
df.drop(labels=0, axis=0, inplace=True)
# use meaningful names
df.rename(columns={'Cód.':'Estado', 'Brasil e Unidade da Federação':'2017', 'Unnamed: 4': '2018'}, inplace=True)
# create specific frames for each year
data_from_2017 = df.loc[:,['Estado', '2017']]
data_from_2018 = df.loc[:,['Estado', '2018']]

world_geo = r'brazil-states.geojson'
brazil_map = folium.Map(location = [0,0], tiles='CartoDB positron')
folium.Choropleth(
    geo_data=world_geo,
    data=data_from_2018,
    columns=['Estado', '2018'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Access to basic sanitation [%]',
).add_to(brazil_map)
brazil_map.show_in_browser()