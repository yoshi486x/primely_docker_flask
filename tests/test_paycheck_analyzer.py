import pprint as pp

from models import pdf_reader



pdfReader = pdf_reader.PdfReader()
pdfReader.load_pdf_filenames()
self.filenames = sorted(pdfReader.filenames)
for filename in self.filenames:
    pdfReader.convert_pdf_to_txt(filename)