import collections
import datetime
import os
import pathlib
import re

import pprint
pp = pprint.PrettyPrinter(indent=2)
TEXT_DIR_PATH = 'data/output/temp'
PAID_INCOME = 'total_earnings' # 差引支給額
PAID_DATE = 'paid_date' # 支払支給日

class DataModel(object):
    """Base model of source data when while being extracted and formatted"""
    def __init__(self, list_data=None, filenames=list):
        self.keys = ['incomes', 'deductions', 'attendances', 'others']
        self.list_data = list_data
        self.dict_data = collections.defaultdict(dict, {key:[] for key in self.keys})
        self.filenames = filenames


class PartitionerModel(DataModel):
    """Read text file and transform it into dict format"""
    def __init__(self, block_count=4):
        super().__init__()
        self.ankers = ['■支給額明細', '■口座情報']
        self.ankerIndexes = [] * block_count
        self.block1, self.block2, self.block3 = list, list, list

    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_data(self, filename):
        """Load data"""

        suffix = '.txt'
        base_dir = self.get_base_dir_path()
        text_file_path = pathlib.Path(base_dir, TEXT_DIR_PATH, filename).with_suffix(suffix)

        with open(text_file_path, 'r') as text_file:
            list_data = text_file.read().splitlines()
        while '' in list_data:
            list_data.remove('')

        self.list_data = list_data

    def value_format_digit(self):
        the_data = self.list_data
        for j, item in enumerate(the_data):
            if type(item) != (int or float):
                if item.replace(',', '').isdigit() is True:
                    the_data[j] = int(item.replace(',', ''))
                elif item.replace('.', '').isdigit() is True:
                    the_data[j] = float(item)

    def define_partitions(self):
        """init ankerIndex for start and end"""
        self.ankerIndexes.append(0)
        for anker in self.ankers:
            self.ankerIndexes.append(self.list_data.index(anker))
        self.ankerIndexes.append(len(self.list_data))

    def partition_data(self):
        """
        Partition one list of data into 3 small lists.
        2 ankers in between are defined by self.ankers = ['■支給額明細', '■口座情報'].
        """

        self.block1 = self.list_data[self.ankerIndexes[0]:self.ankerIndexes[1]]
        self.block2 = self.list_data[self.ankerIndexes[1]:self.ankerIndexes[2]]
        self.block3 = self.list_data[self.ankerIndexes[2]:self.ankerIndexes[3]]

    def update_datamodel(self, name, keys, values):
        self.dict_data[name] = dict(zip(keys, values))

    def self_correlate_block1(self):
        """Update summary and profile categories from block1"""

        # Initialization
        category1 = self.keys[0] # 'profile'
        category2 = self.keys[1] # 'summary'
        sec1 = ['check_type']
        sec2 = ['原籍会社', '社員番号', '氏名']
        sec3 = ['所属部署', '支給年月日', '支給額合計', '控除額合計']
        profile_key = ['comp_name', 'emp_no', 'emp_name', 'dept_name']
        summary_key = ['check_type', 'paid_date', 'total_income', 'total_deduction']
        static_keys = {}
        para1, para2, para3 = [], [], []

        # Where function actually begins
        para1.append(self.block1[0])
        for sec in sec2:
            index = self.block1.index(sec)
            para2.append(self.block1[index + 3])
        for sec in sec3:
            index = self.block1.index(sec)
            para3.append(self.block1[index + 1])

        # Combine 所属部署 extracted in two lines (if so).
        para2.append(para3.pop(0))
        sec2.append(sec3.pop(0))

        # Combine check_type(key) with summary(category)
        sec1.extend(sec3)
        para1.extend(para3)

        # Update extracted key-value pairs
        self.dict_data.update(dict(zip(summary_key, para1)))
        self.dict_data.update(dict(zip(profile_key, para2)))
         
        #exception for 所属部署 with more than two lines
        new_department = []
        startIndex = self.block1.index('所属部署')
        endIndex = self.block1.index('支給年月日') - 1
        lines = abs(endIndex - startIndex)

        if lines > 1:
            for index in startIndex + 1, endIndex:
                new_department.append(self.block1[index])
            self.dict_data['dept_name'] = ''.join(
                new_department)

        # Calculate and append 差引支給額 to dict_data
        total_income = self.dict_data['total_income']
        total_deduction = self.dict_data['total_deduction']

        # deducted_income_key = '差引支給額'
        deducted_income_key = PAID_INCOME
        deducted_income_value = int(total_income) - int(total_deduction)

        self.dict_data.update(
            {deducted_income_key: deducted_income_value})
        # pp.pprint(self.dict_data)

    def self_correlate_block2(self):
        """Initialize paras. Modification needed to simplify code."""
        main_column_names = ['■支給額明細', '■控除額明細', '■勤怠情報', '■その他情報']
        sub_column_names = ['支給項目', '控除項目', '勤怠管理項目', 'その他']
        keys, values, section_anker_names = [], [], []

        """Partition out one-line block to list of keys and values
        input: self.block2
        output: keys, values, section_anker_names
        * All types are list.
        """
        for j, item in enumerate(self.block2):
            """Write cases for if statements"""
            
            if item in main_column_names:
                continue
            elif item in sub_column_names:
                section_anker_name = self.block2[j+1]
                """ Store anker if the section isn't empty. Empty section will 
                eturn int or float from next section."""
                if type(section_anker_name) is str:
                    section_anker_names.append(section_anker_name)
                else:
                    pass
            elif type(item) == int or type(item) == float:
                values.append(item)
            else:
                if item.replace(',', '').rsplit('-',1)[-1].isdigit() is True:
                    values.append(int(item.replace(',', '')))
                elif item.replace('.', '').rsplit('-',1)[-1].isdigit() is True:
                    values.append(float(item))
                elif re.match('\d+等級', item):
                    values.append(str(item))
                else:
                    keys.append(item)

        """Insert func for removing 差引支給額"""
        keys.append(None)
        deducted_income_value = self.dict_data[PAID_INCOME]
        try:
            values.remove(deducted_income_value)
        except:
            pass

        """Combine and partition in sub-blocks
        return: List->section_anker_indexes """
        # Initialize
        categories = ['incomes', 'deductions', 'attendances', 'others']
        slice_manual = collections.defaultdict(dict)

        # Find index_after_smoothing
        section_anker_indexes = []
        for name in section_anker_names:
            section_anker_indexes.append(keys.index(name))
        section_anker_indexes.append(len(keys) - 1)
        slice_borders = []

        # Create index pairs for slices
        for j, index in enumerate(section_anker_indexes):
            if j == len(section_anker_indexes) - 1:
                break
            slice_borders.append((index, section_anker_indexes[j+1]))

        # Partition set of key-values in sections
        """TODO Maybe this creating manual process could be deleted."""
        for category, border in zip(categories, slice_borders):
            slice_manual[category] = border

        # Slice kv and update dict_data
        for category, border in slice_manual.items():
            head, tail = border
            sliced_keys = keys[head:tail]
            sliced_values = values[head:tail]
            self.update_datamodel(category, sliced_keys, sliced_values)
        # pp.pprint(self.dict_data)

    def value_format_date(self):
        thisdate = self.dict_data[PAID_DATE]
        self.dict_data[PAID_DATE] = datetime.datetime.strptime(thisdate, '%Y年%m月%d日').strftime('%Y-%m-%d')

    def value_format_deductions(self, category='deductions'):
        for key, value in self.dict_data[category].items():
            self.dict_data[category][key] = -value

    def value_format_remove_dot_in_keys(self, category='attendances', new_pairs=[], initializer={}):
        """Remove dot from dict keys
        :type category: int
        :type new_pairs: list
        :type initializer: dict
        :rtype: 
        """
        def find_dot_generator():
            for key, value in self.dict_data[category].items():
                yield re.sub('\([^)]*\)', '', key), value
        
        generator = find_dot_generator()
        [new_pairs.append(item) for item in generator]
        self.dict_data[category] = initializer
        self.dict_data[category].update(new_pairs)

    def add_table_name(self):
        date = self.dict_data[PAID_DATE]
        name = 'S_' + date
        named_dict = {name: [self.dict_data]}
        return named_dict

def main():
    pass

if __name__ == "__main__":
    main()