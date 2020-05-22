import pprint as pp

from models import pdf_reader

pdf = pdf_reader.PdfReader()
pdf.convert_pdf_to_txt()