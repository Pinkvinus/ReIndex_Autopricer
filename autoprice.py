import os
import PyPDF2
import re

def get_booksprice(text:str):
    """
    params: A string of text that has been extracted from a pdf receipt
    returns: A list of book title and price pairs. If the price is not in the file, the price is set to None
    """

    spliton1 = 'rykker'
    spliton2 = 'ved gennemgang af bibliotekets udlån kan vi se'

    if has_price(text):
        spliton1 = 'pris\n'
        spliton2 = 'samlet'
    
    books = text.split(spliton1)[1].strip().split(spliton2)[0].strip().split('\n')
    
    bookprice = []
    for b in books:
        b = re.split(r'\s{1,}\d{10,} \d{4}-\d{2}-\d{2}\s', b)
        if float(b[1]) == 2:
            b = [b[0],None]
        bookprice.append(b)
        
    return bookprice

def has_price(text:str)-> bool:
    """
    params:  A text extracted from a PDF receipt
    returns: A bool on whether the receipt contains a price
    """
    if "rykker" in text:
        print(f'The books do not have a price')
        return False
    elif "pris" in text:
        print(f'The books already have a price already has a price')
        return True
    else:
        print('unable to determine if the books have a price')
        return False

def get_PDFreceipt_text(source:str)-> str:
    """
    Params:  A PDF receipt source
    Returns: The text in the pdf
    """
    _,extension = os.path.splitext(source)
    if extension != '.pdf':
        raise TypeError("The file has to be a pdf-file")

    pdfFileObj = open(source, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    if(len(pdfReader.pages)>1):
        print('Warning: There are multiple pages in this pdf. Only the first page will be looked at')
    
    page0 = pdfReader.pages[0].extract_text(0).lower()

    return page0

def lookup_price(booktitle:str):
    with open("ghg books/bookprices.txt") as file:
        lines = [line.rstrip() for line in file]

    if booktitle in lines:
        print(lines)

if __name__ == '__main__':
    sti = "C:/Users/Public/Documents/Regninger/Alma Paldan O'Brien - 3k - inkl. pris.pdf"
    sti2 = "C:/Users/Public/Documents/Regninger/Asta Keogan Schlottmann - 3d.pdf"

    bp = get_booksprice(get_PDFreceipt_text(sti2))

    for book, price in bp:
        if price == None:
            lookup_price(book)
