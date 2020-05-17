"""Define full-analyzer model
TODO raise error when each main process fails
TODO Separate severity of loggers for success and fails"""
import collections
import configparser
import logging
import multiprocessing
import sys
import time

from primely.models import pdf_converter, queueing, recording, txt_converter, visualizing
from primely.views import console, utils

# create logger with '__name__'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler with a defined log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handler(s)
# formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
formatter = logging.Formatter('[{levelname}] {message}', style='{')
ch.setFormatter(formatter)
# add the handler(s) to the logger
logger.addHandler(ch)
# don't allow passing events to higher level loggers
logger.propagate = False

config = configparser.ConfigParser()
config.read('config.ini')


def timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        if 'log_time' in kwargs:
            name = kwargs.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


class QueueingModel(object):

    def __init__(self, filenames=None):
        self.filenames = filenames

    def create_input_queue(self):
        """Create queue of processing data while extracting filenames"""

        try:
            # TODO organize InputQueue func
            input_queue = queueing.InputQueue()
            input_queue.extract_filenames()
            msg = 'Queue is set'
        except:
            self.status = 'error'
            msg = 'Could not set queue'
            logger.critical({
                'status': self.status,
                'msg': msg
            })
        else:
            self.status = 'success'
            msg = 'Queue is set'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        finally:
            pass

        self.filenames = input_queue.get_filename_list()


class ConverterModel(object):
    """Contains functions that process a paycheck object.
    Steps:
    1. Get all pdf file name for paycheck
    2. for each file, proceed Extract and Transform
    """

    def __init__(self, filename, status=None):
        self.filename = filename
        self.status = status
        self.response = collections.defaultdict()

    # @timeit
    def convert_pdf_into_text(self):
        """Utilize pdf_converter module to convert a pdf file to a text file"""
        
        self.pdf_converter = pdf_converter.PdfReader(self.filename)
        input_file_path = self.pdf_converter.get_pdf_dir()
        output_file_path = self.pdf_converter.get_txt_dir()
        self.pdf_converter.convert_pdf_to_txt(input_file_path, output_file_path)

    # @timeit
    def convert_text_into_dict(self):
        """Transform txt data to dict format"""

        try:
            self.txt_converter = txt_converter.PartitionerModel()
            self.txt_converter.load_data(self.filename)
            self.txt_converter.value_format_digit()
            self.txt_converter.define_partitions()
            self.txt_converter.partition_data()
            self.txt_converter.self_correlate_block1()
            self.txt_converter.self_correlate_block2()
            self.txt_converter.value_format_date()
            self.txt_converter.value_format_deductions()
            self.txt_converter.value_format_remove_dot_in_keys()
        except:
            self.status = 'error'
            msg = 'Could not complete text transformation process'
            logger.critical({
                'status': self.status,
                'msg': msg
            })
        else:
            self.status = 'success'
            msg = 'Text transformation complete'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        finally:
            pass
        
        # self.response = self.txt_converter.add_table_name()
        self.response = self.txt_converter.dict_data
        logger.debug({
            'filename': self.filename,
            'data': self.response
        })

    # @timeit
    def convert_dict_into_json(self):
        """Record dict_data to json files"""
        dir_path = config['STORAGE']['JSON']
        utils.setup_output_dir(dir_path)
        dest_info = {
            'filename': self.filename,
            'dir_path': dir_path,
            'file_path': None
        }
        # print('dir_path:', dir_path)
        file_path = None 
        # recording_model = recording.RecordingModel(filename, file_path, dir_path)
        recording_model = recording.RecordingModel(**dest_info)
        # recording_model = recording.RecordingModel(self.filename)
        # output_path = recording_model.get_json_dir()
        recording_model.record_data_in_json(self.response)
        # recording_model.record_dict_in_json(self.response, output_path)


class Dispatcher(object):

    @staticmethod
    def fully_convert(filename):
        coverter = ConverterModel(filename)
        coverter.convert_pdf_into_text()
        coverter.convert_text_into_dict()
        coverter.convert_dict_into_json()

# class FullAnalyzer(QueueingModel, ConverterModel):
class FullAnalyzer(QueueingModel):
    """This is the main process of Primely which can handle multiple 
    pdf files to iterate through all the functionalities that the 
    Primely package ratains."""

    def __init__(self, speak_color='green', filenames=None, dataframe=None):
        super().__init__()
        self.speak_color = speak_color
        self.filenames = filenames
        self.dataframe = dataframe

    def starting_msg(self):
        template = console.get_template('start_proc.txt', self.speak_color)
        print(template.substitute({
            # 'message': 'Check data/output/graphs_and_charts for exported image!'
        }))

    def _setup_output_dir(func):
        """Decorator to set a queue if not loaded"""
        def wrapper(self):
            utils.setup_output_dir(config['STORAGE']['TEXT'])
            utils.setup_output_dir(config['STORAGE']['JSON'])
            # utils.setup_output_dir(config['STORAGE']['GRAPH'])
            utils.setup_output_dir(config['STORAGE']['REPORT'])
            return func(self)
        return wrapper

    def _queue_decorator(func):
        """Decorator to set a queue if not loaded"""
        def wrapper(self):
            if not self.filenames:
                self.create_input_queue()
            return func(self)
        return wrapper

    # @timeit
    @_setup_output_dir
    @_queue_decorator
    def process_all_input_data(self):
        """Use AnalyzerModel to process all PDF data"""

        # Multiprocess
        with multiprocessing.Pool(8) as p:
            r = p.map(Dispatcher.fully_convert, self.filenames)
            logging.debug('executed')
            logging.debug(r)

        # Single-process
        # for filename in self.filenames:
        #     Dispatcher.fully_convert(filename)

    @_queue_decorator
    def create_dataframe_in_time_series(self):
        """Visualize data from json file and export a graph image """
        # TODO Implement sorting, renaming, camouflaging (0/3)
        try:
            visual = visualizing.DataframeFactory()
            visual.classify_json_data_in_categories(visual.categories)
            # visual.sort_table()
            # visual.rename_columns()
            # visual.camouflage_values(True)
            self.dataframe = visual.category_dataframe
            # print(self.dataframe)
        except:
            self.status = 'error'
            msg = 'Chart output failed'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        else:
            self.status = 'success'
            msg = 'Chart output complete'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        finally:
            pass

    @_queue_decorator
    def get_packaged_paycheck_series(self):
        """
        1. Package 3 categories of dataframes in the hash table (self.dataframe)
        2. Get the Package
        """
        try:
            organizer = visualizing.OrganizerModel(**self.dataframe)
            organizer.trigger_update_event()
        except:
            self.status = 'error'
            msg = 'Json export failed'
            logger.info({
                'status': self.status,
                'msg': msg
            })
            raise
        else:
            self.status = 'success'
            msg = 'Json export complete'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        finally:
            return organizer.get_response()

    def export_in_jsonfile(self, response):
        """Export api response of this whole package in a json file"""

        dir_path = config['STORAGE']['REPORT']
        utils.setup_output_dir(dir_path)
        dest_info = {
            'filename': config['FILENAME']['REPORT'],
            'dir_path': dir_path,
            'file_path': None
        }
        recording_model = recording.RecordingModel(**dest_info)
        recording_model.record_data_in_json(response)

    def export_income_timeline(self):
        # Plot graph and save in a image -------------------------------
        try:
            if config['APP'].getboolean('GRAPH_OUTPUT'):
                plotter = visualizing.PlotterModel(self.dataframe)
                plotter.save_graph_to_image()
        except:
            self.status = 'error'
            msg = 'Plotting failed'
            logger.info({
                'status': self.status,
                'msg': msg
            })
            print('Unexpected error:', sys.exc_info()[0])
            raise
        else:
            self.status = 'success'
            msg = 'Plotting complete'
            logger.info({
                'status': self.status,
                'msg': msg
            })
        finally:
            pass

    @_queue_decorator
    def ending_msg(self):
        # TODO include filenames and each processed status in the msg
        template = console.get_template('end_proc.txt', self.speak_color)
        print(template.substitute({
            'message': 'Check data/output/json/paycheck_timechart.json for preprocessed data!'
        }))
