"""
This file lets running test from the directory where test file is located.
"""

import os
import sys

# Register home path
print('############RUNNING context.py###########')
print('Before:', sys.path[0], '\n')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

print('After:', sys.path[0], '\n')
print('############END OF PROCESS###########')


# import packages for testing
from primely.models import paycheck_analyzer, pdf_reader, queueing, recording, tailor, visualizing


