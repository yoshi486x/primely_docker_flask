import os
import sys

print(sys.path, '\n')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path, '\n')

from primely.models import pdf_reader


