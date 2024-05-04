# Description: This script is used to split a PDF file into multiple PDF files.
from PyPDF2 import PdfReader, PdfWriter

input_pdf = 'original.pdf'
output_pdf = 'new_book.pdf'
pageStart = 0
pageEnd = 2

def split_pdf(input_pdf, start_page, end_page, output_pdf):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        for page_num in range(start_page, end_page + 1):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)
            
            
split_pdf(input_pdf, pageStart, pageEnd, output_pdf)