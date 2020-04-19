import os
import sys
print(sys.path, '\n')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path, '\n')


# from pathlib import Path
# Path(__file__).resolve().parent.parent

# import sample
from primely.models import pdf_reader



# from models import pdf_reader
