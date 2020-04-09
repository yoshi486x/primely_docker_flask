"""Define full-analyzer model
TODO raise error when each main process fails
TODO Separate severity of loggers for success and fails"""
import collections
import logging
import sys

from primely.models import pdf_reader, recording, tailor, visualizing
from primely.views import console

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


class QueueingModel(object):

    def __init__(self, filenames=None):
        self.filenames = filenames

    def create_input_queue(self):
        """Create queue of processing data while extracting filenames"""

        try:
            # TODO organize InputQueue func
            inputQueue = pdf_reader.InputQueue()
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

        self.filenames = inputQueue.load_pdf_filenames()


class ConverterModel(object):
    """Contains functions that process a paycheck object.
    Steps:
    1. Get all pdf file name for paycheck
    2. for each file, proceed Extract and Transform
    """
    def __init__(self, status=None):
        self.dict_data = collections.defaultdict()
        self.status = status

    def convert_pdf_into_text(self, filename):
        """Utilize pdf_reader module to convert a pdf file to a text file"""
        
        pdfReader = pdf_reader.PdfReader()
        input_file = pdfReader.get_pdf_dir(filename)
        output_file = pdfReader.get_txt_dir(filename)
        pdfReader.convert_pdf_to_txt(input_file, output_file)

    def convert_text_into_dict(self, filename):
        """Transform txt data to dict format"""

        try:
            text_tailor = tailor.PartitionerModel()
            text_tailor.load_data(filename)
            text_tailor.value_format_digit()
            text_tailor.define_partitions()
            text_tailor.partition_data()
            text_tailor.self_correlate_block1()
            text_tailor.self_correlate_block2()
            text_tailor.value_format_date()
            text_tailor.value_format_deductions()
            text_tailor.value_format_remove_dot_in_keys()
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
        
        # self.dict_data = text_tailor.add_table_name()
        self.dict_data = text_tailor.dict_data
        logger.debug({
            'filename': filename,
            'data': self.dict_data
        })

    def record_dict_data(self, filename):
        """Record dict_data to json files"""

        recording_model = recording.RecordingModel(filename)
        recording_model.record_data_in_json(self.dict_data)


class FullAnalyzer(QueueingModel, ConverterModel):
    """This is the main process of Primely which can handle multiple 
    pdf files to iterate through all the functionalities that the 
    Primely package ratains."""

    def __init__(self, speak_color='green', filenames=None):
        super().__init__()
        self.speak_color = speak_color
        self.filenames = filenames

    def starting_msg(self):
        template = console.get_template('start_proc.txt', self.speak_color)
        print(template.substitute({
            # 'message': 'Check data/output/graphs_and_charts for exported image!'
        }))

    def _queue_decorator(func):
        """Decorator to set a queue if not loaded"""
        def wrapper(self):
            if not self.filenames:
                self.create_input_queue()
            return func(self)
        return wrapper

    @_queue_decorator
    def process_all_input_data(self):
        """Use AnalyzerModel to process all PDF data"""
        
        for j, filename in enumerate(self.filenames):
            try:
                self.convert_pdf_into_text(filename)
                self.convert_text_into_dict(filename)
                self.record_dict_data(filename)
            except:
                self.status = 'error'
                msg = 'File conversion failed'
                logger.critical({
                    'status': self.status,
                    'index': j,
                    'filename': filename,
                    'msg': msg
                })
            else:
                self.status = 'success'
                msg = ''
                logger.info({
                    'status': self.status,
                    'index': j,
                    'filename': filename,
                    'msg': msg
                })
            finally:
                pass

    @_queue_decorator
    def create_dataframe_in_time_series(self):
        """Visualize data from json file and export a graph image """
        # TODO: Separate dataframe formatting and exporting to image
        try:
            visual = visualizing.CompoundModel()
            visual.create_base_table()
            visual.sort_table()
            visual.rename_columns()
            visual.camouflage_values(True)
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

        # Plot graph -------------------------------
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read('config.ini')
            if config['APP']['GRAPH_OUTPUT'] is True:
                visual.save_graph_to_image()
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

        # Export in a json file -------------------------------
        # try:
        #     import configparser
        #     if config['APP']['GRAPH_OUTPUT'] is True:
        #         visual.save_graph_to_image()
        # except:
        #     self.status = 'error'
        #     msg = 'Plotting failed'
        #     logger.info({
        #         'status': self.status,
        #         'msg': msg
        #     })
        # else:
        #     self.status = 'success'
        #     msg = 'Plotting complete'
        #     logger.info({
        #         'status': self.status,
        #         'msg': msg
        #     })
        # finally:
        #     pass


    @_queue_decorator
    def ending_msg(self):
        # TODO include filenames and each processed status in the msg
        template = console.get_template('end_proc.txt', self.speak_color)
        print(template.substitute({
            'message': 'Check data/output/graphs_and_charts for exported image!'
        }))
