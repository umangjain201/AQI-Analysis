#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# Reading csv file to dataframe

# In[20]:


airq_df = pd.read_csv('city_day.csv')
airq_df


# In[21]:


airq_df.info()


# Coverting 'Date' columns to Date Format

# In[22]:


airq_df['Date'] = pd.to_datetime(airq_df['Date'])


# Extracting columns Year, Month, Day, Weekday from column 'Date' & insertion

# In[23]:


airq_df.insert(loc = 2, column = 'Year', value = pd.DatetimeIndex(airq_df.Date).year)
airq_df.insert(loc = 3, column = 'Month', value = pd.DatetimeIndex(airq_df.Date).month)
airq_df.insert(loc = 4, column = 'Day', value = pd.DatetimeIndex(airq_df.Date).day)
airq_df.insert(loc = 5, column = 'Weekday', value = pd.DatetimeIndex(airq_df.Date).weekday)


# Creating dataframe for 'Delhi Analysis'

# In[24]:


delhi_df = airq_df[airq_df.City == 'Delhi']
delhi_df.info()


# Monthly AQI & Pollutants Analysis

# In[25]:


delhi_df.groupby('Month')['AQI'].mean()


# In[26]:


import calendar as cld
month_name = []
for month in delhi_df.Month.unique():
    month_name.append(cld.month_abbr[month])
    

plt.rcParams['figure.figsize'] = (12,7)
sns.set_style('whitegrid')
columns1 = ['PM2.5','PM10','AQI']
for column in columns1:
        plt.plot( month_name,delhi_df.groupby('Month')[column].mean(), marker = 'o', label = column)
plt.legend()
plt.xlabel('Month')
plt.ylabel('Mean AQI')
sns.set_style('whitegrid')


# Monthly Pollutants Analysis

# In[27]:


#from labellines import labelLines
#import matplotx
columns2 = ['NO','NO2','NOx','NH3','SO2','O3','Toluene','Xylene', 'CO','Benzene']
plt.rcParams['figure.figsize'] = (12,7)
for column in columns2:
    if(column in ['CO','Benzene','Xylene']):
        plt.plot( month_name,delhi_df.groupby('Month')[column].mean(), marker = 'X', label = column, ls = '--')
    else:
        plt.plot( month_name,delhi_df.groupby('Month')[column].mean(), marker = 'o', label = column)
plt.legend()
plt.xlabel('Month')
plt.ylabel('Mean AQI')
#labelLines(plt.gca().get_lines(), zorder=2.5)
#matplotx.line_labels()


# Month Analysis Per Year

# In[28]:


delhi_df.groupby(['Month','Year'])['AQI'].mean().unstack().plot(
    xlabel = 'Month', ylabel = 'Mean AQI', figsize = (16, 10), marker = 'X');


# Analysis - PM2.5 & PM10 relationship with AQI

# In[29]:


for column in ['PM2.5','PM10']:
     sns.regplot(x=delhi_df.groupby('Month')['AQI'].mean(), y = delhi_df.groupby(['Month'])[column].mean(), label = column, scatter=True)
        #sns.scatterplot(x=delhi_df.groupby(['Month'])['AQI'].mean(), y = delhi_df.groupby(['Month'])[column].mean(), s=100, label = column)
plt.ylabel('Particulate Matter')
plt.legend();


# Analysis - Other Pollutants relationship with AQI

# In[30]:


for column in columns2:
    #sns.scatterplot(x=delhi_df.groupby(['Month'])['AQI'].mean(), y = delhi_df.groupby(['Month'])[column].mean(), s=100, label = column)
    sns.regplot(x=delhi_df.groupby('Month')['AQI'].mean(), y = delhi_df.groupby(['Month'])[column].mean(), label = column, scatter=False)
plt.ylabel('Pollutants')
plt.legend();


# Persistent AQI scores

# In[31]:


plt.hist(delhi_df.AQI);


# Daywise AQI Analysis

# In[32]:


g = sns.barplot(x = 'Weekday' , y = 'AQI', data = delhi_df, color = 'blue');
sns.lineplot(x = 'Weekday', y = 'AQI', data = delhi_df, color = 'red');
plt.ylabel('Mean AQI');
plt.xlabel('Day of Week');
g.set_xticklabels(list(cld.day_name));

