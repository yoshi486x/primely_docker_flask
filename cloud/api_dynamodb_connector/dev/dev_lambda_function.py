import collections
import json
import numpy as np
import os
import pathlib
import pandas as pd

import pprint
pp = pprint.PrettyPrinter()

import config

FILENAMES = config.FILENAMES
JSON_DIR_PATH = config.JSON_DIR_PATH


def _convert_decimals(items):

    def _decimal_default_proc(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        else:
            raise TypeError
    
    return json.dumps(items, default=_decimal_default_proc, ensure_ascii=False)
    # return json.dumps(items, ensure_ascii=False)


class ExtracterModel(object):
    def __init__(self, items=[]):
        self.items = items

    def import_json_files(self):
        for filename in FILENAMES:
            file_path = pathlib.Path(JSON_DIR_PATH, filename).with_suffix('.json')
            with open(file_path, 'r') as json_file:
                dict_data = json.load(json_file)
            self.items.append(dict_data)
        return self.items


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
            dates, keys, values = [], [], []
            date = item['paid_date']
            for key, value in item[category].items():
                dates.append(date)
                keys.append(key)
                values.append(value)
            df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
            dataframes.append(df)
        df = pd.concat(dataframes)
        table = pd.pivot_table(df, index='date', columns='type', values='value', fill_value=0)
        rows = {'rows': list(table.index)}
        columns = {'columns': list(table.columns)}
        # v_array = table.to_numpy()
        v_array = table.values
        values = {'values': v_array.tolist()}

        self.response[category].update(rows)
        self.response[category].update(columns)
        self.response[category].update(values)
        return print('{} transformation complete.'.format(category))

def main(earliest=None, latest=None, categories=None):
    categories = ['incomes', 'deductions', 'attendances']
    extracter = ExtracterModel()
    items = extracter.import_json_files()
    items = _convert_decimals(items)
    # print(items)
    items = json.loads(items)
    # print('paid_date:', items[0]['paid_date'])
    # print('item:', items[0])

    transformer = TransformerModel(categories, items)
    transformer.get_timechart()

    response = json.dumps(transformer.response, ensure_ascii=False)
    # print(transformer.response)
    # print(response)
    # return print('COMPLETE')
    return response



if __name__ == "__main__":
    res = main()
    print(res)
