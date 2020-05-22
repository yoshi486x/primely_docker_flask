import os
import pprint as pp
import sys

# path = sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print('path:', path)

# from models import tailor

if __package__ is None or __package__ == '':
    # uses current directory visibility
    import foo
else:
    # uses current package visibility
    from . import foo
    
# ALOGO_PASSED_FILE_INDEX = [4]
# FILENAMES = [
#     '1300_1614120_K_20181025',
#     '1300_1614120_K_20181122',
#     '1300_1614120_K_20181225',
#     '1300_1614120_K_20190125',
#     '1300_1614120_K_20190225',
#     '1300_1614120_K_20190325',
#     '1300_1614120_K_20190425',
#     '1300_1614120_K_20190524',
#     '1300_1614120_K_20190625',
#     '1300_1614120_K_20190725',
#     '1300_1614120_K_20190823',
#     '1300_1614120_K_20190925',
#     '1300_1614120_K_20191025',
#     '1300_1614120_K_20191125',
#     '1300_1614120_K_20191225'
#  ]

# filenames = FILENAMES[5]
# # filenames = FILENAMES[4:6]

# for filename in filenames:
#     text_tailor = tailor.PartitionerModel()

#     text_tailor.load_data(filename)
#     text_tailor.define_partitions()
#     text_tailor.partition_data()
#     text_tailor.self_correlate_block1()
#     text_tailor.self_correlate_block2()
#     text_tailor.self_correlate_block3()
#     text_tailor.value_format_date()
#     text_tailor.value_format_digit()
#     text_tailor.value_format_deductions()
#     text_tailor.value_format_remove_dot_in_keys()
#     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
#     pp.pprint(text_tailor.dict_data)

