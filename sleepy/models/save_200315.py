# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import json
import numpy as np
import os
import pandas as pd
import pathlib


# %%
JSON_DIR_PATH = 'data/output/json'
PAID_DATE = 'paid_date'
CATEGORY = 'income'
BASE_DIR = '/Users/dev-yoshiki/Hobby/paycheck_reader'
EMP_NO = 9999999
JSON_DIR_PATH = '/Users/dev-yoshiki/Hobby/paycheck_reader/data/output/json'
JSON_FILES = ['1300_1614120_K_20180425.json', '1300_1614120_K_20180525.json', '1300_1614120_K_20180625.json', '1300_1614120_K_20180725.json', '1300_1614120_K_20180824.json', '1300_1614120_K_20180925.json', '1300_1614120_K_20181025.json', '1300_1614120_K_20181122.json', '1300_1614120_K_20181225.json', '1300_1614120_K_20190125.json', '1300_1614120_K_20190225.json', '1300_1614120_K_20190325.json', '1300_1614120_K_20190425.json', '1300_1614120_K_20190524.json', '1300_1614120_K_20190625.json', '1300_1614120_K_20190725.json', '1300_1614120_K_20190823.json', '1300_1614120_K_20190925.json', '1300_1614120_K_20191025.json', '1300_1614120_K_20191125.json', '1300_1614120_K_20191225.json', '1300_1614120_K_20200124.json', '1300_1614120_K_20200225.json']


# %%
dataframes = []
for filename in JSON_FILES:
    dates, keys, values, indexes = [], [], [], []

    file_path = pathlib.Path(JSON_DIR_PATH, filename)
    with open(file_path, 'r') as json_file:
        dict_data = json.load(json_file)

    """Single key extraction"""
    dates, keys, values = [], [], []
    date = dict_data[PAID_DATE]
    for key, value in dict_data['incomes'].items():
        values.append(value)
        keys.append(key)
        dates.append(date)
    df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
    dataframes.append(df)

df = pd.concat(dataframes)


# %%
# Sort data by ranking values statistically.
table = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)
table.loc['不足日数時間精算'] = table.loc['不足日数時間精算'].abs()
table.replace(0, np.nan, inplace=True)

## total, mean, std
table['total'] = table.filter(regex='\d{4}-\d{2}-\d{2}').sum(axis=1)
table['total'] = table['total'].astype(int).round(0)
table['mean'] = table.filter(regex='\d{4}-\d{2}-\d{2}').mean(axis=1)
table['mean'] = table['mean'].astype(int).round(0)
table = table.fillna(0)
table['std'] = table.filter(regex='\d{4}-\d{2}-\d{2}').std(axis=1)
table['std'] = (table['std'] / table['mean'] * 100).astype(float).round(2)

# norm
Total = table['total'].sum()
table['norm'] = (table['total'] / Total * 100).round(2)
print('Total:', Total)
print('sum(norm):', table['norm'].sum())

# sort by std


table[['total', 'mean', 'std', 'norm']]


# %%
table[['mean','total']]

# %% [markdown]
# 

# %%
newTable = table.transpose()
EN_TYPE = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
        'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'LIma', 'Mike', 
        'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra']

col_num = len(table.columns)
EN_TYPE = EN_TYPE[:col_num]
col_dict = dict(zip(table.columns, EN_TYPE))
newTable = table.rename(columns=col_dict)
newTable


# %%


