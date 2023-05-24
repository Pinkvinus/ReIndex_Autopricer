import requests
import os
import selenium
import PyPDF2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_pdf(url:str):
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False

def write_in_pdf(pdfFileObj):
    # creating a pdf file object
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    if(len(pdfReader.pages)>1):
        print('Warning: There are multiple pages in this pdf. Only the first page will be looked at')
    
    page = pdfReader.pages[0]
    text = page.extract_text(0)

    print(str.split(text, "\n"))
    








if __name__ == '__main__':
    # URL from which pdfs to be downloaded
    #URL = 'https://learnit.itu.dk/mod/resource/view.php?id=152145'
    #get_pdf(URL)
    pdfFileObj = open('welcome.pdf', 'rb')
    write_in_pdf(pdfFileObj)

    







