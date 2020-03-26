"""Define full-analyzer model"""
import collections
import pprint as pp

from models import pdf_reader, recording, tailor, visualizing
from views import console


class AnalyzerModel(object):
    """Handle data model on analyzing process
    Steps:
    1. Get all pdf file name for paycheck
    2. for each file, proceed Extract and Transform
    """
    def __init__(self, 
        status=None, pdf_files=None, txt_files=None, **kwargs):
        self.status = status
        self.pdf_files = pdf_files# Not implemented yet
        self.txt_files = txt_files# Not implemented yet
        self.dict_data = collections.defaultdict()

    def convert_pdf_into_text(self, filename):
        
        pdfReader = pdf_reader.PdfReader()
        input_file = pdfReader.get_pdf_dir(filename)
        output_file = pdfReader.get_txt_dir(filename)
        pdfReader.convert_pdf_to_txt(input_file, output_file)
        # Extract filename and txt_file, here.

    def convert_text_into_dict(self, filename):
        """Transform txt data to dict format"""

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
        # self.dict_data = text_tailor.add_table_name()
        self.dict_data = text_tailor.dict_data
        # pp.pprint(self.dict_data)

    def record_dict_data(self, filename):
        """Record dict_data to multiple file/db formats (json, mongodb, mysql)"""

        recording_model = recording.RecordingModel(filename, self.status)
        recording_model.record_data_in_json(self.dict_data)
        if self.status:
            recording_model.record_data_to_mongo(self.dict_data)


class FullAnalyzer(AnalyzerModel):

    def __init__(self, db='MongoDB', speak_color='green', filenames=None):
        super().__init__()
        self.db = db
        self.speak_color = speak_color
        self.filenames = filenames

    def ask_for_db_activation(self):
        while True:
            template = console.get_template('db_activation.txt', self.speak_color)
            is_yes = input(template.substitute({
                'db': self.db}))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                self.status = True
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                self.status = False
                break
    
    def check_mongodb_activation(self):
        """Create instance for Recording models (MongoDB)"""

        mongo_model = recording.MongoModel(None)
        if not mongo_model.get_mongo_profile():
            template = console.get_template('db_response.txt', self.speak_color)
            print(template.substitute({'db': self.db}))
            self.status = False
        else:
            self.status = True

    def create_input_queue(self):
        """Create queue of processing data while extracting filenames"""

        inputQueue = pdf_reader.InputQueue()
        self.filenames = inputQueue.load_pdf_filenames()

    def process_all_data(self):
        """Use AnalyzerModel to process all PDF data"""
        
        self.create_input_queue()
        for filename in self.filenames:
            self.convert_pdf_into_text(filename)
            self.convert_text_into_dict(filename)
            self.record_dict_data(filename)

    def visualize_income_timechart(self):
        """Visualize data from json file and export a graph image """

        visual = visualizing.VisualizingModel(None)
        visual.create_base_table()
        visual.rename_columns()
        visual.sort_table()
        visual.camouflage_values(True)
        visual.save_graph_to_image()

        # dialog
        template = console.get_template('process_finished.txt', self.speak_color)
        print(template.substitute())