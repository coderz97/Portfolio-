'''
CS665, Summer24  Project 

Sreya Jain Tobji

'''

import PyPDF2
import os

#function to split and convert each page of the uploaded pdf into separate text files
def convert(pdf_path, output_folder):
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extracting text from each page of the PDF
            for page_number, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()

                # Create a text file for each page
                text_filename = os.path.join(output_folder, f"DOC_{page_number}")
                with open(text_filename, 'w', encoding='utf-8') as text_file:
                    # Write the text to the text file
                    text_file.write(text)




