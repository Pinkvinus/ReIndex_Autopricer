import requests
import os
import PyPDF2

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By


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

def get_price(text:str):
    
    return 123

def get_books(text:str):
    """
    params: A string of text that has been extracted from a pdf receipt
    """

    spliton1 = 'rykker'
    spliton2 = 'ved gennemgang af bibliotekets udlån kan vi se'

    if has_price(text):
        spliton1 = 'pris\n'
        spliton2 = 'samlet'
    
    books = text.split(spliton1)[1].strip().split(spliton2)[0].strip()
    books = books.split('\n')


    print(f'These are the books:{books}!!! wow such pretty books')

def has_price(text:str)-> bool:
    if "rykker" in text:
        print(f'The books do not have a price')
        return False
    elif "pris" in text:
        print(f'The books already have a price already has a price')
        return True
    else:
        print('unable to determine if the books have a price')
        return False

def write_price_in_pdf(pdfFileObj):
    # creating a pdf file object
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    if(len(pdfReader.pages)>1):
        print('Warning: There are multiple pages in this pdf. Only the first page will be looked at')
    
    page0 = pdfReader.pages[0].extract_text(0).lower()

    print(page0)

    get_books(page0)
    
    texts = str.split(page0, "\n")
    








if __name__ == '__main__':
    # URL from which pdfs to be downloaded
    #URL = 'https://learnit.itu.dk/mod/resource/view.php?id=152145'
    #get_pdf(URL)

    sti = "C:/Users/Public/Documents/Regninger/Alma Paldan O'Brien - 3k - inkl. pris.pdf"
    sti2 = "C:/Users/Public/Documents/Regninger/Asta Keogan Schlottmann - 3d.pdf"

    pdfFileObj = open(sti2, 'rb')
    write_price_in_pdf(pdfFileObj)










