"""This is the raw script used for api_dynamodb_connector.py"""

import collections
import numpy as np
import pandas as pd


class TransformerModel(object):

    def __init__(self, categories, items):
        self.categories = categories
        self.items = items
        self.response = collections.defaultdict(dict)
        if len(self.response) == 0:
            self.init_response()

    def init_response(self):
        for category in self.categories:
            self.response.update({category: {}})

    def get_timechart(self):
        for category in self.categories:
            self.transform_item(category, self.items)
    
    def transform_item(self, category, items):
        dataframes = []
        for item in items:
            if type(item) == dict:
                dates, keys, values = [], [], []
                date = item['paid_date']
                for key, value in item[category].items():
                    dates.append(date)
                    keys.append(key)
                    values.append(value)
                df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
                dataframes.append(df)
            else:
                print('This is not an object from dynamodb.')
        df = pd.concat(dataframes)
        table = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)
        rows = {'rows': list(table.index)}
        columns = {'columns': list(table.columns)}
        # v_array = table.to_numpy()
        v_array = table.values
        values = {'values': v_array.tolist()}

        self.response[category].update(rows)
        self.response[category].update(columns)
        self.response[category].update(values)
        return print('{} transformation complete.'.format(category))