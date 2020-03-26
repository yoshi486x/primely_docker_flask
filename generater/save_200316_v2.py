# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import json
import numpy as np
import os
import pandas as pd
import pathlib


# %%
BASE_DIR = '/Users/dev-yoshiki/Hobby/paycheck_reader'
CATEGORIES = ['incomes', 'deductions', 'attendances']
CATEGORY = 'incomes'
EMP_NO = 9999999
JSON_DIR_PATH = '/Users/dev-yoshiki/Hobby/paycheck_reader/data/output/json'
JSON_FILES = ['1300_1614120_K_20180425.json', '1300_1614120_K_20180525.json', '1300_1614120_K_20180625.json', '1300_1614120_K_20180725.json', '1300_1614120_K_20180824.json', '1300_1614120_K_20180925.json', '1300_1614120_K_20181025.json', '1300_1614120_K_20181122.json', '1300_1614120_K_20181225.json', '1300_1614120_K_20190125.json', '1300_1614120_K_20190225.json', '1300_1614120_K_20190325.json', '1300_1614120_K_20190425.json', '1300_1614120_K_20190524.json', '1300_1614120_K_20190625.json', '1300_1614120_K_20190725.json', '1300_1614120_K_20190823.json', '1300_1614120_K_20190925.json', '1300_1614120_K_20191025.json', '1300_1614120_K_20191125.json', '1300_1614120_K_20191225.json', '1300_1614120_K_20200124.json', '1300_1614120_K_20200225.json']
OUTPUT_PATH = '/Users/dev-yoshiki/Hobby/paycheck_reader/dev_frontend/json/incomes.json'
PAID_DATE = 'paid_date'


# %%
Response = {'incomes': {}, 'deductions': {}, 'attendances': {}}


# %%
def updateRes(response, category, table):
    print('response:', response)
    rows = {'rows': list(table.index)}
    columns = {'columns': list(table.columns)}
    # v_array = table.to_numpy()
    v_array = table.values
    values = {'values': v_array.tolist()}

    # print('response:', response)
    # TODO:Output to one file
    response[category].update(rows)
    response[category].update(columns)
    response[category].update(values)
    print(response)
    return response


# %%
def create_table(category):
    dataframes = []
    for filename in JSON_FILES:
        dates, keys, values, indexes = [], [], [], []

        file_path = pathlib.Path(JSON_DIR_PATH, filename)
        with open(file_path, 'r') as json_file:
            dict_data = json.load(json_file)

        """Single key extraction"""
        dates, keys, values = [], [], []
        date = dict_data[PAID_DATE]
        for key, value in dict_data[category].items():
            values.append(value)
            keys.append(key)
            dates.append(date)
        df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
        dataframes.append(df)
    df = pd.concat(dataframes)
    return df


# %%
# Create 'incomes' table 
# -----------------------------------------------------------------------
category = CATEGORIES[0]
df = create_table(category)
# pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)


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
table = table.sort_values(by=['std'], ascending=True)

# add rank params
table['sum_rank'] = table['total'].rank(ascending=False).astype(int).round(0)
table['std_rank'] = table['std'].rank(ascending=True).astype(int).round(0)
table['norm_rank'] = table['norm'].rank(ascending=False).astype(int).round(0)
table['rank_avg'] = table.filter(regex='_rank$').mean(axis=1).astype(float).round(2)
table['Ranking'] = table['rank_avg'].rank(ascending=True).astype(int).round(0)

# sort by std
table = table.sort_values(by=['Ranking'], ascending=True)

print(table[['total', 'mean', 'std', 'norm', 'sum_rank', 'std_rank', 'norm_rank', 'rank_avg', 'Ranking']])

# roll-back negative income
table.loc['不足日数時間精算'] = table.loc['不足日数時間精算'] * -1

# extract sorted table
st = table.filter(regex='\d{4}-\d{2}-\d{2}')
st


# %%
# Rename indexes in English
js_row = st.index.values.tolist()
JS_ROW = ['基本給', 'Smart&Fun!支援金', '新卒住宅補助', '時間外勤務手当', '通勤手当*', '遡及差額', 'その他支給(課税加算)', '休日勤務手当', '資格取得(奨励金)', '不足日数時間精算', '深夜勤務手当']
EN_ROW = ['base', 'supp', 'rent', 'over', 'trans', 'past', 'other', 'off', 'cert', 'defi', 'night']

convTable = dict(zip(JS_ROW, EN_ROW))
print(convTable)
en_table = st.rename(index=convTable)
en_table


# %%
# Tweek values
demoTable = en_table.copy()
en_row = en_table.index.values.tolist() # EN_ROW
WEIGHT = [0.0389, 0.023, 0.0045, 0.0029, 0.0122, 0.0312, 0.012, 0.033, 0.013, 0.00412]

weiTable = dict(zip(EN_ROW, WEIGHT))

for key, val in weiTable.items():
    print(key, val)
    demoTable.loc[key] = (demoTable.loc[key] * val).astype(int).round(0)
demoTable


# %%
# Update 'incomes' in response
response = updateRes(Response, category, demoTable)
response


# %%
# Create 'deduction' table
# -----------------------------------------------------------------------
cat = CATEGORIES[1]
df = create_table(cat)
df = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)
# ddf


# %%
# Rename index in english
ja_row = df.index.values.tolist()
ja_row
JA_ROW = ['その他控除(月例･一時)', '住民税', '健康保険料', '厚生年金保険料', '所得税', '社食利用料', '還付徴収額', '雇用保険料']
EN_ROW = ['other_ded', 'resid_tax', 'health_ins', 'pension_ins', 'income_tax', 'cafe_use', 'refund_bil', 'emp_ins' ]

convTable = dict(zip(JA_ROW, EN_ROW))
print(convTable)
sdf = df.rename(index=convTable)
sdf


# %%
# Tweek values
demoTable = sdf.copy()
en_row = demoTable.index.values.tolist() # EN_ROW
WEIGHT = [0.0389, 0.023, 0.0045, 0.0029, 0.0122, 0.0312, 0.012, 0.033]

weiTable = dict(zip(EN_ROW, WEIGHT))

for key, val in weiTable.items():
    print(key, val)
    demoTable.loc[key] = (demoTable.loc[key] * val).astype(int).round(0)
demoTable


# %%
# Update response deduc 
# print('Response:', Response)
# print('cat:', cat)
# print('ddf:', ddf)
response = updateRes(Response, cat, demoTable)
response


# %%
# Create 'attendance' table
# -----------------------------------------------------------------------
cat = CATEGORIES[2]
df = create_table(cat)
df = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)
df


# %%
# Rename index in english
ja_row = df.index.values.tolist()
ja_row
JA_ROW = ['代休取得日数', '休日勤務時間数', '年休取得日数', '所定内勤務時間数', '所定勤務日数', '所定勤務時間数', '早退回数', '早退時間', '時間外勤務時間数', '深夜勤務時間数']
EN_ROW = ['make-up_ad', 'holi_wd', 'holi_ad', 'within_wh', 'speci_wd', 'speci_wh', 'early_c', 'early_h', 'over_wh', 'night_wh']

convTable = dict(zip(JA_ROW, EN_ROW))
print(convTable)
rdf = df.rename(index=convTable)
rdf


# %%
# Tweek values
demoTable = rdf.copy()
en_row = demoTable.index.values.tolist() # EN_ROW(10)
WEIGHT = [1, 1, 1, 150, 20, 155, 1, 2, 5, 1]

weiTable = dict(zip(EN_ROW, WEIGHT))

for key, val in weiTable.items():
    print(key, val)
    demoTable.loc[key] = val
demoTable


# %%
# Update response 'attend' 
# print('Response:', Response)
# print('cat:', cat)
# print('ddf:', ddf)
response = updateRes(Response, cat, demoTable)
response


# %%
# Export combined data to json file
# -----------------------------------------------------------
OUTPUT_PATH = '/Users/dev-yoshiki/Hobby/paycheck_reader/dev_frontend/json/demo_data_200316.json'
jsn = json.dumps(response, ensure_ascii=False)
with open(OUTPUT_PATH, 'w') as json_file:
    json_file.write(jsn)
jsn


# %%


