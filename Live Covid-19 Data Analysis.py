# %%
#Get live data from Website
from bs4 import BeautifulSoup
import lxml
import requests
import urllib.request

#Data Processing
import pandas as pd

#data Visualization
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import chart_studio
import plotly
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot

#For Map Visualization
import folium

# %%
pyo.init_notebook_mode(connected=True)
cf.go_offline()

# %%
"""
## Get Live Data from website
"""

# %%
demo = urllib.request.urlopen('https://www.mygov.in/corona-data/covid19-statewise-status')
soup = BeautifulSoup(demo,"lxml")

# %%
"""
## Get Time of Retrive a data
"""

# %%
tabledata = soup.find('div', class_='content clearfix')
time = tabledata.find('div', class_='field-item')
print('The Covid-19 data updated on',time.text)

# %%
"""
### Create a list to Store a data
"""

# %%
State_Name = ['demo']
Total_confirmed = ['demo']
Cured = ['demo']
Death = ['demo']

# %%
"""
## Save data in List
"""

# %%
for con in tabledata.find_all('div', class_='content'):
    
    item1 = con.find('div', class_='field field-name-field-select-state field-type-list-text field-label-above')
    data_state = item1.find('div', class_='field-items')
    State_Name.append(data_state.text)


    item2 = con.find('div', 
                     class_='field field-name-field-total-confirmed-indians field-type-number-integer field-label-above')
    data_cases = item2.find('div', class_='field-items')
    Total_confirmed.append(data_cases.text)


    item3 = con.find('div', 
                     class_='field field-name-field-cured field-type-number-integer field-label-above')
    data_cured = item3.find('div', class_='field-items')
    Cured.append(data_cured.text)


    item4 = con.find('div', 
                     class_='field field-name-field-deaths field-type-number-integer field-label-above')
    data_death = item4.find('div', class_='field-items')
    Death.append(data_death.text)

# %%
"""
## Create a DataFrame form list
"""

# %%
Data_table = {'STATE NAME':State_Name, 'TOTAL CONFIRMED':Total_confirmed, 'CURED/DISCHARGED/MIGRATED':Cured,
             'DEATH':Death}

# %%
covid_india = pd.DataFrame(Data_table)

# %%
covid_india = covid_india.drop(0)
covid_india = covid_india.reset_index(drop=True)

# %%
covid_india.dtypes

# %%
covid_india['TOTAL CONFIRMED'] = covid_india['TOTAL CONFIRMED'].astype(int)
covid_india['CURED/DISCHARGED/MIGRATED'] = covid_india['CURED/DISCHARGED/MIGRATED'].astype(int)
covid_india['DEATH'] = covid_india['DEATH'].astype(int)

# %%
covid_india.head()

# %%
covid_india['ACTIVE CASES'] = covid_india['TOTAL CONFIRMED'] - covid_india['CURED/DISCHARGED/MIGRATED'] - covid_india['DEATH']

# %%
covid_india.head()

# %%
"""
## Analysis Data in Numerical Format
"""

# %%
covid_india.style.background_gradient(cmap = 'Reds')

# %%
total_active = covid_india.groupby('STATE NAME')['TOTAL CONFIRMED'].sum().sort_values(ascending = False).to_frame()

total_active.head()

# %%
total_active.style.background_gradient(cmap = 'Reds')

# %%
"""
## Analysis Data in Graph Format
"""

# %%
covid_india.iplot(kind='bar',x='STATE NAME',y='TOTAL CONFIRMED',
                  title='State wise Covid-19 Cases',xTitle='State',yTitle='Total Cases')

# %%
fig=px.bar(covid_india,x="STATE NAME",y="TOTAL CONFIRMED",color='TOTAL CONFIRMED',title='Total cases in India')
fig.show()

# %%
fig=px.bar(covid_india,x="STATE NAME",y="DEATH",color='DEATH',title='Total Death in India')
fig.show()

# %%
fig=px.bar(covid_india,x="STATE NAME",y="CURED/DISCHARGED/MIGRATED",color='CURED/DISCHARGED/MIGRATED',
           title='Total Cases Close in India')
fig.show()

# %%
plt.figure(figsize=(10,5),dpi=200)

#plt.plot(covid_india['STATE NAME'], covid_india['TOTAL CONFIRMED'], label='Math marks', color='r')
plt.plot(covid_india['STATE NAME'], covid_india['CURED/DISCHARGED/MIGRATED'], label='CURED/DISCHARGED',marker='*', color='m')
plt.plot(covid_india['STATE NAME'], covid_india['DEATH'],marker='*', label='DEATH', color='r')
plt.plot(covid_india['STATE NAME'], covid_india['ACTIVE CASES'],marker='*', label='ACTIVE CASES', color='g')

plt.xticks(covid_india['STATE NAME'], rotation=90)
plt.xlabel('States')
plt.ylabel('No of Cases')
plt.title('State wise Cases')

plt.legend()
plt.show()



# %%
"""
### Insert a Latitude and Longitude in main DataFrame
"""

# %%
covid_india.head()

# %%
map_data = pd.read_csv('Indian Coordinates.csv')

# %%
map_data.head()

# %%
covid_india = pd.merge(covid_india, map_data, on='STATE NAME')

# %%
covid_india.head()

# %%


# %%
"""
## Analysis Data in Map Format
"""

# %%
#folium.Map()

# %%
map1 = folium.Map(location=[25,80],zoom_start=4.5,tiles='openstreetmap')

for lat,long,value,name in zip(covid_india['Latitude'],covid_india['Longitude'],
                                covid_india['TOTAL CONFIRMED'],covid_india['STATE NAME']):
   
    folium.CircleMarker([lat,long],radius=value*0.01,popup=('<strong>State</strong>: '+str(name).capitalize()+'<br>''<strong>Total Cases</strong>: '+ str(value)+ '<br>'),
                        color='red',fill_color='red',fill_opacity=0.1).add_to(map1)
    

# %%
map1