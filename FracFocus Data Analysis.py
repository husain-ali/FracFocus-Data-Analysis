#!/usr/bin/env python
# coding: utf-8

# <h2>Index</h2><br>
# <ul><li><a href="#Correlation">Correlation between different variables in the dataset using Pairplot and Heatmap</a></li>
#     <li><a href="#Ing and Percent">Ingredients and their PercentHFJob and PercentHighAdditive</a></li>
#     <li><a href="#Ing and Purpose">Ingredients and their Purpose</a></li>
#     <li><a href="#HF and States">Hydraulic Fracturing Jobs across different States</a></li>
#     <li><a href="#Suppliers">Most Frequently Contracted Suppliers for Fracturing jobs</a></li>
#     <li><a href="#Time">Time Analysis across some Registries</a></li>
#     <li><a href="#Geopd Wells">Plotting all the Federal and Indian Wells using Geopandas</a></li>
#     <li><a href="#Geopd Ing">Ingredients used across various locations</a></li>
#     <li><a href="#Calculation">Calculation of Volume based on ingredients</a></li>
# </ul>

# In[1]:


# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

import geopandas as gpd
from shapely.geometry import Point, Polygon


# In[2]:


# Reading all the required datasets

df_ffr1 = pd.read_csv("FracFocusRegistry_1.csv")
df_ffr2 = pd.read_csv("FracFocusRegistry_2.csv")
df_ffr3 = pd.read_csv("FracFocusRegistry_3.csv")
df_ffr4 = pd.read_csv("FracFocusRegistry_4.csv")
df_ffr5 = pd.read_csv("FracFocusRegistry_5.csv")
df_ffr6 = pd.read_csv("FracFocusRegistry_6.csv")
df_ffr7 = pd.read_csv("FracFocusRegistry_7.csv")
df_ffr8 = pd.read_csv("FracFocusRegistry_8.csv")
df_ffr9 = pd.read_csv("FracFocusRegistry_9.csv")
df_ffr10 = pd.read_csv("FracFocusRegistry_10.csv")
df_ffr11 = pd.read_csv("FracFocusRegistry_11.csv")
df_ffr12 = pd.read_csv("FracFocusRegistry_12.csv")
df_ffr13 = pd.read_csv("FracFocusRegistry_13.csv")
df_ffr14 = pd.read_csv("FracFocusRegistry_14.csv")
df_ffr15 = pd.read_csv("FracFocusRegistry_15.csv")
df_ffr16 = pd.read_csv("FracFocusRegistry_16.csv")
df_ffr17 = pd.read_csv("FracFocusRegistry_17.csv")
df_ffr18 = pd.read_csv("FracFocusRegistry_18.csv")

warnings.filterwarnings("ignore")


# In[3]:


# Combining these datasets
df_ffr = pd.concat([df_ffr1, df_ffr2, df_ffr3, df_ffr4, df_ffr5, df_ffr6, df_ffr7, 
                    df_ffr8, df_ffr9, df_ffr10, df_ffr11, df_ffr12, df_ffr13, df_ffr14, 
                    df_ffr15, df_ffr16, df_ffr17, df_ffr18], ignore_index=True)


# In[4]:


# Looking into the dataset

df_ffr.info()


# In[5]:


df_ffr1.info()


# In[6]:


df_ffr2.info()


# In[7]:


df_ffr17.info()


# In[8]:


# All the above 3 datasets have following columns with null values
# Source                     0 non-null float64
# DTMOD                      0 non-null float64
# SystemApproach             0 non-null float64
# IsWater                    0 non-null float64
# PurposePercentHFJob        0 non-null float64
# PurposeIngredientMSDS      0 non-null float64
# These can be easily omitted

# PurposeKey                 is primary key
# UploadKey                  is pk
# IngredientKey              is pk
# These can be omitted

# IngredientMSDS             
# MassIngredient             
# DisclosureKey              
# These are unexplained in readme, but have significant data


# <h3><a id="Correlation">Correlation between different variables in the dataset using Pairplot and Heatmap</a></h3>

# In[9]:


# Finding correaltion using pairplot
# Only considering Registry 1 for faster processing

sns.pairplot(df_ffr1[["APINumber","StateNumber","CountyNumber","TVD"]])
plt.figure(figsize=(40,40))
plt.show()


# In[10]:


# Finding correaltion using pairplot
# Only considering Registry 1 for faster processing

sns.pairplot(df_ffr1[["TotalBaseWaterVolume","TotalBaseNonWaterVolume","PercentHighAdditive","PercentHFJob"]])
plt.figure(figsize=(40,40))
plt.show()


# In[11]:


# Finding correaltion using heatmap

corr = df_ffr.corr()

fig, ax = plt.subplots(figsize=(7,7))  
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, ax=ax, cmap="YlGnBu")
plt.show()


# <h3><a id="Ing and Percent">Ingredients and their PercentHFJob and PercentHighAdditive</a></h3><br>Based on the correlation heatmap, we will first find out realtionship between PercentHFJob and PercentHighAdditive. This can be achived by finding both of the feature's individual relationship with their ingredients.<br>Only the top 20 ingredients will be considered for both the cases.<br><br>Since IngredientName contains messy data, it is cleaned by the following manner:

# In[12]:


# Caplitalizing the Ingredient Names in order to avoid duplicate enrties

df_ffr['IngredientName'] = df_ffr['IngredientName'].str.capitalize()


# In[13]:


# Finding out relationship between Ingredients with PercentHFJob

df_ffr.groupby(['IngredientName'])['PercentHFJob'].describe().sort_values(by = 'count', ascending = False).head(20)


# In[14]:


# Finding out relationship between Ingredients with PercentHighAdditive

df_ffr.groupby(['IngredientName'])['PercentHighAdditive'].describe().sort_values(by = 'count', ascending = False).head(20)


# In[15]:


# Determining correlation between PercentHFJob and PercentHighAdditive

round(df_ffr['PercentHighAdditive'].corr(df_ffr['PercentHFJob']),4)


# There is a similar trend in which the oil and gas wells which use the top 20 frequently occurring ingredients. Even the Percentages in HFJob and High Additive show similar trend as shown above.

# <h3><a id="Ing and Purpose">Ingredients and their Purpose</a></h3><br>Now we will determine for which most frequently used purposes are the top ingredients used. This data can be highly informative for users to know what could be the actual reason behind using any ingredient. <br>Note that it simply shows the purpose for those ingredients just based on frequency and there could be other reasons why a particular ingredient is used for.

# In[16]:


# Determining ingredients and their most frequent purposes

df_ffr.groupby(['IngredientName'])['Purpose'].describe().sort_values(by = 'count', ascending = False).head(20)


# <h3><a id="HF and States">Hydraulic Fracturing Jobs across different States</a></h3><br>Now, determing Statewise Hydraulic Fracturing jobs that took place over all the years in all the datasets.<br>The states could have been directly determined from the attribute StateName but since the entries for this feature contained a lot of spelling mistakes and different name formats eg. two character state name were used and the whole state name was also used.<br>But to carry out analysis efficiently, these names were determined from the StateNumber column of the dataset.<br>The state numbers were obtained from the mappings provided by Wikipedia on different API Well Numbers.

# In[17]:


# Mapping State Numbers to State Names, creating an additional column called DerivedStateName

State_Code = {
1: 'Alabama',
2: 'Arizona',
3: 'Arkansas',
4: 'California',
5: 'Colorado',
6: 'Connecticut',
7: 'Delaware',
8: 'District of Columbia',
9: 'Florida',
10: 'Georgia',
11: 'Idaho',
12: 'Illinois',
13: 'Indiana',
14: 'Iowa',
15: 'Kansas',
16: 'Kentucky',
17: 'Louisiana',
18: 'Maine',
19: 'Maryland',
20: 'Massachusetts',
21: 'Michigan',
22: 'Minnesota',
23: 'Mississippi',
24: 'Missouri',
25: 'Montana',
26: 'Nebraska',
27: 'Nevada',
28: 'New Hampshire',
29: 'New Jersey',
30: 'New Mexico',
31: 'New York',
32: 'North Carolina',
33: 'North Dakota',
34: 'Ohio',
35: 'Oklahoma',
36: 'Oregon',
37: 'Pennsylvania',
38: 'Rhode Island',
39: 'South Carolina',
40: 'South Dakota',
41: 'Tennessee',
42: 'Texas',
43: 'Utah',
44: 'Vermont',
45: 'Virginia',
46: 'Washington',
47: 'West Virginia',
48: 'Wisconsin',
49: 'Wyoming',
50: 'Alaska',
51: 'Hawaii',
55: 'Alaska Offshore',
56: 'Pacific Coast Offshore',
60: 'Northern Gulf of Mexico',
61: 'Atlantic Coast Offshore'
}

df_ffr["DerivedStateName"] = df_ffr['StateNumber'].map(State_Code)


# In[18]:


# Plotting the top 10 states for which Hydraulic Fracturing was carried out

df_ffr['DerivedStateName'].value_counts()[:10].sort_values(ascending=True).plot(kind='barh', 
                                            align='center', title='Jobs across various states') 
plt.xlabel("Count") 
plt.ylabel("States")

plt.show() 


# In[19]:


# Percentage wise ploting the same data as above using a pie chart

df_ffr['DerivedStateName'].value_counts()[:10].sort_values(ascending=True).plot(kind='pie', 
                                            startangle = 90, shadow = True, autopct='%1.0f%%', radius = 2,
                                            y='Statewise Jobs Contracted')
plt.legend(loc='best', bbox_to_anchor=(1.5, 1.5))
plt.show()


# <h3><a id="Suppliers">Most Frequently Contracted Suppliers for Fracturing jobs</a></h3><br>Now we will find out which suppliers were most frequently contracted.<br>The Supplier data needed to be cleansed because punctuations, white spaces and case diffrence caused duplicate entries.<br>We will finally plot a pie chart to find out which suppliers were mostly contracted.

# In[20]:


# Cleaning the Supplier data

df_ffr_copy = pd.DataFrame()

df_ffr_copy['Supplier'] = df_ffr['Supplier'].str.lower()
df_ffr_copy['Supplier'] = df_ffr_copy['Supplier'].replace("?","")
df_ffr_copy['Supplier'] = df_ffr_copy['Supplier'].str.strip()
df_ffr_copy['Supplier'] = df_ffr_copy['Supplier'].str.replace(r'[^\w\s]', '')

df_ffr['Supplier'] = df_ffr_copy['Supplier']


# In[21]:


# Plotting pie chart for Suppliers that were contracted more than 50,000 times

df_ffr['Supplier'].value_counts()[df_ffr['Supplier'].value_counts()>50000].plot(kind='pie', 
                                                startangle = 0, shadow = True, autopct='%1.0f%%', radius = 2)
plt.legend(loc='best', bbox_to_anchor=(1.5, 1.5))
plt.show()


# <h3><a id="Time">Time Analysis across some Registries</a></h3><br>Now we will determine what were the minimum and maximum start dates and the end dates of these jobs.<br>These times were calculated based on individual registries for faster data processing because converting a column to datetime takes a lot of time. However, with better GPUs, this can be done at a faster pace even on the entire dataset.

# In[22]:


# Displaying Minimum and Maximum Start and End dates for Registry 1 data

print("Registry 1 - Job StartDate Max - ", pd.to_datetime(df_ffr1['JobStartDate']).max())
print("Registry 1 - Job StartDate Min - ", pd.to_datetime(df_ffr1['JobStartDate']).min())
print("Registry 1 - Job EndDate Max - ", pd.to_datetime(df_ffr1['JobEndDate']).max())
print("Registry 1 - Job EndDate Min - ", pd.to_datetime(df_ffr1['JobEndDate']).min())


# In[23]:


# Displaying Minimum and Maximum Start and End dates for Registry 2 data

print("Registry 2 - Job StartDate Min - ", pd.to_datetime(df_ffr2['JobStartDate']).min())
print("Registry 2 - Job StartDate Max - ", pd.to_datetime(df_ffr2['JobStartDate']).max())
print("Registry 2 - Job EndDate Min - ", pd.to_datetime(df_ffr2['JobEndDate']).min())
print("Registry 2 - Job EndDate Max - ", pd.to_datetime(df_ffr2['JobEndDate']).max())


# In[24]:


# Displaying Minimum and Maximum Start and End dates for Registry 17 data

print("Registry 17 - Job StartDate Min - ", pd.to_datetime(df_ffr17['JobStartDate']).min())
print("Registry 17 - Job StartDate Max - ", pd.to_datetime(df_ffr17['JobStartDate']).max())
print("Registry 17 - Job EndDate Min - ", pd.to_datetime(df_ffr17['JobEndDate']).min())
print("Registry 17 - Job EndDate Max - ", pd.to_datetime(df_ffr17['JobEndDate']).max())


# In[25]:


# Calculating difference in dates by converting default format of Job Start and End dates to datetime
# and then subtracting Job end date from job start date

df_ffr1['DiffernceInDates'] = pd.to_datetime(df_ffr1['JobEndDate']) - pd.to_datetime(df_ffr1['JobStartDate'])


# In[26]:


df_ffr1.DiffernceInDates.describe()


# In[27]:


df_ffr1[df_ffr1['DiffernceInDates'] == df_ffr1.DiffernceInDates.max()]


# In[28]:


df_ffr1[df_ffr1['DiffernceInDates'] == df_ffr1.DiffernceInDates.max()].TVD.describe()


# The difference in dates can also help us understanding using domain knowledge the reason why it takes a majority of the job to be completed in 0 days and why is a job that even took in this Registry data 618 days.

# <h3><a id="Geopd Wells">Plotting all the Federal and Indian Wells using Geopandas</a></h3><br>
# First we will be creating a Geopanda DataFrame from the original dataset and then we will be plotting the Federal and Indian Wells throughout the United States.<br>
# We will then plot bar charts of the most frequently Federal and Indian Wells in which hydraulic fracturing is carried out.

# In[29]:


# Creating a Geopanda dataframe similar to that of the combined dataset 

get_ipython().run_line_magic('matplotlib', 'inline')

geometry = [Point(xy) for xy in zip(df_ffr.Longitude, df_ffr.Latitude)]
crs = {'init': 'epsg:4326'}
street_map = gpd.read_file('C:\\Users\\range\\FracFocus\\UScounties\\UScounties.shp')

new_locs = gpd.GeoDataFrame(df_ffr, crs=crs, geometry=geometry)
new_locs.head()


# In[30]:


# Plotting the GeoPanda DataFrame with Federal and Indian Wells

fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = 0.8, color='grey')
new_locs[new_locs['FederalWell']==True].plot(ax=ax, markersize=20, color='blue', marker='o', label='Federal Well')
new_locs[new_locs['IndianWell']==True].plot(ax=ax, markersize=20, color='red', marker='^', label='Indian Well')
plt.title('Federal and Indian Wells accross different regions')
plt.legend(prop={'size': 15})


# In[31]:


# Plotting a Horizontal Bar Chart of the top frequently Federal wells in which fracturing was carried out

df_ffr.loc[df_ffr['FederalWell'] == True].WellName.value_counts()[df_ffr.loc[df_ffr['FederalWell'] == True].WellName.value_counts()>130].sort_values(ascending=True).plot(kind='barh', title='Top 8 Federal Wells in which Hydraulic Fracturing was carried out')
plt.xlabel("Count") 
plt.ylabel("Well Name")

plt.show() 


# In[32]:


# More details about these Federal Wells

df_ffr.loc[df_ffr['FederalWell'] == True].WellName.describe()


# In[33]:


# Plotting a Horizontal Bar Chart of the top frequently Federal wells in which fracturing was carried out

df_ffr.loc[df_ffr['IndianWell'] == True].WellName.value_counts()[df_ffr.loc[df_ffr['IndianWell'] == True].WellName.value_counts()>87].sort_values(ascending=True).plot(kind='barh', title='Top 8 Indian Wells in which Hydraulic Fracturing was carried out')
plt.xlabel("Count") 
plt.ylabel("Well Name")

plt.show() 


# In[34]:


# More details about these Indian Wells

df_ffr1.loc[df_ffr1['IndianWell'] == True].WellName.describe()


# <h3><a id="Geopd Ing">Ingredients used across various locations</a></h3><br>We will now find out in which locations were some commonly used ingredients used. This will also be done using GeoPandas but only for Registry 1.<br>
# This analysis can be used for rare ingredients to find out where were they used.

# In[35]:


# Creating a Geopanda dataframe similar to that of the combined dataset 

geometry = [Point(xy) for xy in zip(df_ffr1.Longitude, df_ffr1.Latitude)]
crs = {'init': 'epsg:4326'}
street_map = gpd.read_file('C:\\Users\\range\\FracFocus\\UScounties\\UScounties.shp')

new_locs = gpd.GeoDataFrame(df_ffr1, crs=crs, geometry=geometry)


# Plotting the GeoPanda DataFrame with some ingredients

fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = 0.8, color='grey')
new_locs[new_locs['IngredientName']=='Water'].plot(ax=ax, markersize=20, color='blue', marker='o', label='H2O')
new_locs[new_locs['IngredientName']=='Hydrochloric acid'].plot(ax=ax, markersize=20, color='red', marker='^', label='HCL')
new_locs[new_locs['IngredientName']=='Methanol'].plot(ax=ax, markersize=20, color='yellow', marker='o', label='CH3OH', alpha = 0.1)
plt.title('Ingredients used across different regions')
plt.legend(prop={'size': 15})


# This shows where exactly were these ingredients used.

# <h3><a id="Calculation">Calculation of Volume based on ingredients</a></h3>

# In[5]:


# Calculation of volume based on ingredients

def calculate_volume(row):
    if row['IngredientName'] == 'Water':
        return row['TotalBaseWaterVolume'] * row['PercentHFJob']
    else:
        return row['TotalBaseNonWaterVolume'] * row['PercentHFJob']

df_ffr['Volume_by_ingredients'] = 0
df_ffr['Volume_by_ingredients'] = df_ffr.apply(calculate_volume, axis=1)


# In[6]:


# Viewing the information calculated above

df_ffr.Volume_by_ingredients.describe()


# This can be used to find volumes of individual ingredients that can be used for further analysis.
