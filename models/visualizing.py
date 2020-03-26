import collections
import json
import numpy as np
import os
import pandas as pd
import pathlib
import pprint
pp = pprint.PrettyPrinter(indent=4, width=20)

JSON_DIR_PATH = 'data/output/json'
GRAPHS_DIR_PATH = 'data/output/graphs_and_charts'
INCOME_GRAPH_NAME = 'income_timechart.png'

PAID_DATE = 'paid_date'

class JsonModel(object):
    def __init__(self, filename, json_file):
        if not json_file:
            json_file = self.get_json_file_path(filename)
        if not os.path.exists(json_file):
            pathlib.Path(json_file).touch()
        self.filename = filename
        self.json_file = json_file


class VisualizingModel(object):

    def __init__(self, filenames, base_dir=None, dataframe=None, figure=None):
        if not base_dir:
            base_dir = self.get_base_dir_path()
        self.base_dir = base_dir
        if not filenames:
            filenames = self.get_json_file_path() 
        self.filenames = filenames
        self.dataframe = dataframe
        self.figure = figure
        self.graphs = INCOME_GRAPH_NAME

    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_json_file_path(self):
        """Set json file path.
        Use json path if set in settings, otherwise use default.
        
        :type filename: str
        :rtype json_file_path: str
        """
        json_file_path = None
        try:
            import settings
            if settings.JSON_FILE_PATH:
                json_file_path = settings.JSON_FILE_PATH
        except ImportError:
            pass

        filenames = []
        json_full_dir_path = pathlib.Path(self.base_dir, JSON_DIR_PATH)

        if json_file_path is None:
            for item in os.listdir(json_full_dir_path):
                filenames.append(item)
        return filenames

    def create_base_table(self):
        """Create base tablefor """
        df = self.dataframe
        dataframes = []

        # Loop
        """TODO: dict data loaded from json file will have some broken structures.
        In detail, values with blank space are separeted into multiple columns"""
        for filename in self.filenames:
            dates, keys, values, indexes = [], [], [], []

            file_path = pathlib.Path(JSON_DIR_PATH, filename)
            with open(file_path, 'r') as json_file:
                # data = json.load(json_file)
                dict_data = json.load(json_file)
            
            """Exclude table name from json file"""
            # for key in data.keys():
            #     name = key
            # dict_data = data[name].pop()

            """Single key extraction"""
            dates, keys, values = [], [], []
            # pp.pprint(dict_data)
            date = dict_data[PAID_DATE]
            for key, value in dict_data['incomes'].items():
                values.append(value)
                keys.append(key)
                dates.append(date)
            df = pd.DataFrame({'date': dates, 'type': keys, 'income': values})
            dataframes.append(df)

        # Combine tables of each json file
        df = pd.concat(dataframes)
        table = pd.pivot_table(df, index='date', columns='type', values='income', fill_value=0)
        
        self.dataframe = table

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

    def sort_table(self):

        try:
            from models import sorting
        except:
            import sorting

        df = sorting.sort_table(self.dataframe)
        self.dataframe = df

    def save_graph_to_image(self):
        file_path = pathlib.Path(GRAPHS_DIR_PATH, self.graphs)
        ax = self.dataframe.plot(
            figsize=(15, 10), kind='bar', stacked=True, grid=True, sharey=False,
            title='Income breakdown **Sample data was used for this graph**',
            )
        ax.set_ylabel('amount of income [yen]')
        fig = ax.get_figure()
        fig.savefig(file_path)


def main():
    visual = VisualizingModel(None)
    print(visual.filenames)
    visual.create_base_table()
    visual.rename_columns()
    visual.sort_table()
    visual.camouflage_values(True)
    visual.save_graph_to_image()


if __name__ == "__main__":
    main()