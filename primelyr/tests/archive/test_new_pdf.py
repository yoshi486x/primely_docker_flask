import os
import pathlib
import pprint

from models import full_analyser, tailor, pdf_reader

pp = pprint.PrettyPrinter(indent=2)
TXT_DIR_PATH = 'data/output/temp'
SUCCESSOR = '1300_1614120_K_20190225.txt'
FAILURE = '1300_1614120_K_20180425.txt'


base_dir = os.path.dirname(os.path.abspath(__file__))
input_full_dir_path = pathlib.Path(base_dir, TXT_DIR_PATH)

filenames = os.listdir(input_full_dir_path)
filenames.sort()
# [print(filename) for filename in filenames]

while True:
    print('Which filnames do you whan to test with?')
    isanswer = int(input("[1]Full  [2]Successor  [3]Failure \n"))
    print('isanswer:', isanswer)
    
    if isanswer in [1, 2, 3]:
        break

if isanswer == 2:
    # filenames = list(SUCCESSOR)
    filenames = [SUCCESSOR]
elif isanswer == 3:
    filenames = [FAILURE]
else:
    pass
print('\nFilanames:', filenames, '\n')


istailor = tailor.PartitionerModel()

for filename in filenames:
    text_tailor = tailor.PartitionerModel()
    text_tailor.load_data(filename)
    text_tailor.value_format_digit()
    text_tailor.define_partitions()
    text_tailor.partition_data()
    text_tailor.self_correlate_block1()
    pp.pprint(text_tailor.dict_data)
    text_tailor.self_correlate_block2()
    text_tailor.value_format_date()
    text_tailor.value_format_deductions()
    text_tailor.value_format_remove_dot_in_keys()