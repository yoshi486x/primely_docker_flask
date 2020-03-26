# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import json
import os
import numpy as np
import pandas as pd
import pathlib

import config



FILENAMES = config.FILENAMES
JSON_DIR_PATH = config.JSON_DIR_PATH
CATEGORY = 'attendances'


items = []
for filename in FILENAMES:
    file_path = pathlib.Path(JSON_DIR_PATH, filename).with_suffix('.json')
    with open(file_path, 'r') as json_file:
        dict_data = json.load(json_file)
    items.append(dict_data)
print(dict_data)

dataframes = []
for item in items:
    dates, keys, values = [], [], []
    date = item['paid_date']
    # dates.append(date)
    for key, value in item[CATEGORY].items():
        dates.append(date)
        keys.append(key)
        values.append(value)
#     print('dates:', dates)
#     print('keys:', keys)
#     print('values:', values)
    df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
    dataframes.append(df)

df = pd.concat(dataframes)
print(df)

table = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)

rows = list(table.index)
columns = list(table.columns)
print(rows, len(rows))
print(columns, len(columns))
v_array = table.values
# v_array = table.to_numpy()
values = v_array.tolist()
res_dict = {CATEGORY: {}}
res_dict[CATEGORY].update(rows)
res_dict[CATEGORY].update(columns)
res_dict[CATEGORY].update(values)

print(res_dict)



