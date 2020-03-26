#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os
import numpy as np
import pandas as pd
import pathlib

import config


# In[2]:


FILENAMES = config.FILENAMES
JSON_DIR_PATH = config.JSON_DIR_PATH


# In[3]:


items = []
for filename in FILENAMES:
    file_path = pathlib.Path(JSON_DIR_PATH, filename).with_suffix('.json')
    with open(file_path, 'r') as json_file:
        dict_data = json.load(json_file)
    items.append(dict_data)


# In[4]:


# Check inside items
item = items[10]
item['paid_date']


# In[5]:


# Test by a single item.
dataframes = []
item = items[10]

dates, keys, values = [], [], []
date = item['paid_date']
# dates.append(date)
for key, value in item['incomes'].items():
    dates.append(date)
    keys.append(key)
    values.append(value)
print('dates:', dates)
print('keys:', keys)
print('values:', values)
df = pd.DataFrame({'date': dates, 'type': keys, 'income': values})
dataframes.append(df)
pd.concat(dataframes)


# In[6]:


dataframes = []
for item in items:
    dates, keys, values = [], [], []
    date = item['paid_date']
    # dates.append(date)
    for key, value in item['incomes'].items():
        dates.append(date)
        keys.append(key)
        values.append(value)
#     print('dates:', dates)
#     print('keys:', keys)
#     print('values:', values)
    df = pd.DataFrame({'date': dates, 'type': keys, 'income': values})
    dataframes.append(df)

pd.concat(dataframes)
    


# In[10]:


df = pd.concat(dataframes)
table = pd.pivot_table(df, index='date', columns='type', values='income', fill_value=0)
table


# In[17]:


rows = list(table.index)
columns = list(table.columns)
print(rows, len(rows))
print(columns, len(columns))


# In[16]:


values = table.to_numpy()
values

