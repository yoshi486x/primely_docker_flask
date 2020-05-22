import collections
import configparser
import json
import numpy as np
import os
import pandas as pd
import pathlib

# TODO uncomment out the utils and rollback line 29 and 30
try:
    from primely.views import utils
except:
    pass

# import global parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
JSON_DIR_PATH = config['STORAGE']['JSON']
GRAPHS_DIR_PATH = config['STORAGE']['GRAPH']
INCOME_GRAPH_NAME = config['FILENAME']['GRAPH']

PAID_DATE = 'paid_date'

class JsonLoaderModel(object):
    def __init__(self, filename, dir_path, dict_data=None):
        self.dir_path = dir_path
        if not dict_data:
            dict_data = self._get_dict_data(filename)
        self.dict_data = dict_data

    def _get_dict_data(self, filename):
        file_path = pathlib.Path(self.dir_path, filename)
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

class CreateTimechartModel(object):
    def __init__(self, base_dir=None, filenames=None):
        if not base_dir:
            base_dir = utils.get_base_dir_path(__file__)
            # base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_dir = base_dir
        if not filenames:
            filenames = self._get_json_filenames()
        self.filenames = filenames

    def _get_json_filenames(self, filenames=[]):
        """Set json file path.
        Use given json filenames if set on calls, otherwise use default.
        
        :type filenames: list
        :rtype filenames: list
        """

        json_full_dir_path = pathlib.Path(self.base_dir, JSON_DIR_PATH)
        if len(filenames) == 0:
            for item in os.listdir(json_full_dir_path):
                filenames.append(item)
        return filenames


class CreateBaseTable(object):
    def __init__(self, dataframe=None):
        self.dataframe = dataframe

    def create_base_table(self, category):
        """Create base table"""

        df = self.dataframe
        dataframes = []

        # Loop
        """TODO dict data loaded from json file will have some broken structures.
        In detail, values with blank space are separeted into multiple columns"""
        for filename in self.filenames:
            dates, keys, values, indexes = [], [], [], []

            # Get hash table from json
            json_loader = JsonLoaderModel(filename, JSON_DIR_PATH)
            dict_data = json_loader.dict_data

            # Extract parameters by category type
            dates, keys, values = [], [], []

            date = dict_data[PAID_DATE]
            for key, value in dict_data[category].items():
                values.append(value)
                keys.append(key)
                dates.append(date)
            df = pd.DataFrame({'date': dates, 'type': keys, 'value': values})
            dataframes.append(df)

        # Combine tables of each json file
        df = pd.concat(dataframes)
        # print(df)
        # table = pd.pivot_table(df, index='date', columns='type', values='income', fill_value=0)
        table = pd.pivot_table(df, index='type', columns='date', values='value', fill_value=0)
        # print(table)
        self.dataframe = table

        return self.dataframe


class DataframeFactory(CreateTimechartModel, CreateBaseTable):

    def __init__(self, categories=['incomes', 'deductions', 'attendances'],
            dataframeList=[], category_dataframe={'incomes': None, 'deductions': None, 'attendances': None}):
        CreateTimechartModel.__init__(self)
        CreateBaseTable.__init__(self)
        self.categories = categories
        self.dataframeList = dataframeList
        self.category_dataframe = category_dataframe

    def classify_json_data_in_categories(self, categories=None):
        for category, dataframe in self.category_dataframe.items():
            df = self.create_base_table(category)
            self.category_dataframe[category] = df

    # TODO Implement code on AWS to this function.
    def sort_table(self):

        try:
            from primely.models import sorting
        except:
            import sorting

        df = sorting.sort_table(self.dataframe)
        self.dataframe = df

    def rename_columns(self):
        renames = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
             'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'LIma', 'Mike', 
             'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra']
        df = self.dataframe

        col_num = len(df.columns)
        renames = renames[:col_num]
        col_dict = dict(zip(df.columns, renames))
        self.dataframe = df.rename(columns=col_dict)

    def camouflage_values(self, camouflage=False):

        if camouflage is True:
            try:
                from models import camouflage
            except:
                try:
                    import camouflage
                except:
                    return
            self.dataframe = camouflage.camouflage(self.dataframe)


RESPONSE_TEMPLATE = {'incomes': {}, 'deductions': {}, 'attendances': {}}
class OrganizerModel(object):
    def __init__(self, dataframe=None, response=RESPONSE_TEMPLATE,
             *args, **kwargs):
        self.dataframe = dataframe
        self.request = kwargs
        self.response = response

    def trigger_update_event(self):
        for category, dataframe in self.request.items():
            self.update_response(category, dataframe)
    
    def update_response(self, category, dataframe):
        # v_array = self.dataframe.to_numpy()
        v_array = dataframe.values
        rows = {'rows': list(dataframe.index)}
        columns = {'columns': list(dataframe.columns)}
        values = {'values': v_array.tolist()}

        self.response[category].update(rows)
        self.response[category].update(columns)
        self.response[category].update(values)

    def get_response(self):
        return self.response


class PlotterModel(object):

    def __init__(self, dataframe=None):
        self.dataframe = dataframe

    def save_graph_to_image(self):
        file_path = pathlib.Path(GRAPHS_DIR_PATH, INCOME_GRAPH_NAME)
        ax = self.dataframe.plot(
            figsize=(15, 10), kind='bar', stacked=True, grid=True, sharey=False,
            title='Income breakdown **Sample data was used for this graph**',
            )
        ax.set_ylabel('amount of income [yen]')
        fig = ax.get_figure()
        fig.savefig(file_path)

def main():
    categories = ['incomes', 'deductions', 'attendances']
    visual = DataframeFactory()
    visual.classify_json_data_in_categories(visual.categories)
    
    # visual.create_base_table()
    # visual.rename_columns()
    # visual.sort_table()
    # visual.camouflage_values(True)
    
    # myDataframe = visual.dataframe

    organizer = OrganizerModel(**visual.category_dataframe)
    organizer.trigger_update_event()
    organizer.export_response_in_json()

    # df = visual.dataframe
    # plotter = PlotterModel(df)
    # plotter.save_graph_to_image()

if __name__ == "__main__":
    main()