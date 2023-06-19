import os
import PyPDF2
import re
from fpdf import FPDF
import tkinter
from tkinter import filedialog

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
        print(f'The book(s) in this file does not have a price')
        return False
    elif "pris" in text:
        print(f'The book(s) in this file have a price')
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

def load_hashmap():
    """
    returns: A hashmap that contains the title of the books as a key, and the price of the book as a value
    """
    BPDict = {}
    with open("ghg books/bookprices.txt") as file:
        lines = [line.rstrip() for line in file]
        print(lines)
    for bp in lines:

        print(bp)
        book, price = bp.split(";")
        BPDict[book.strip()] = price.strip()
    return BPDict
    
def lookup_price(booktitle:str):
    """
    params: Takes the title of the book and looks up the price
    retuns: The price of a book
    """
    BPDict = load_hashmap()

    if booktitle in BPDict:
        print(f"The book \"{booktitle}\" has a recorded price: {BPDict[booktitle]}.")
        return BPDict[booktitle]
    else:
        print(f"The book \"{booktitle}\" does not have a recorded price.")
        return enter_price(booktitle)

def enter_price(booktitle:str):
    """
    Takes a booktitle, and prompts an entry to the file in which the prices are recorded.
    params:  Booktitle of the book that needs a price
    returns: The new price of the book
    """
    print(f"Enter the price of the book and press [enter].(This can always be changed in the file bookprices.txt)")
    while True:
        price = input(f"Price for \"{booktitle}\":").strip()
        try:
            price = float(price)
            write_price_to_file(booktitle, price)
            return price
        except:
            print(f"The price given \"{price}\" is not a number. (This programme only accepts numbers with \".\" and not \",\")")

def write_price_to_file(booktitle:str, price):
    """
    Appends the title and the book price to a file
    params: booktitle of a book, the price of the given book
    """
    with open("ghg books/bookprices.txt", "a") as fileobj:
        fileobj.write(f"{booktitle} ; {price}\n")
    print(f"\"{booktitle}\" has been recorded with the price: {price}")  

def write_prices_pdf(path:str, prices):
    """
    Takes a file path to a pdf that doesn't have prices and writes the prices in the pdf.
    Params: A file path to a pdf
    """

    reader_base = PyPDF2.PdfReader(path)
    page_base = reader_base.pages[0]

    
    pdf = FPDF()
    pdf.add_page()

    x = 90
    y = 71 #+ 4 for hver item i listen

    pdf.set_xy(x, 63.5)
    pdf.set_font('arial', '', 8.0)
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt="Pris", border=0)

    for p in prices: 
        pdf.set_xy(x, y)
        pdf.set_font('arial', '', 6.0)
        pdf.cell(ln=0, h=5.0, align='L', w=0, txt=p, border=0)
        y+=4
    
    pdf.output('ghg books/Placeholder.pdf', 'F')
    
    reader = PyPDF2.PdfReader("ghg books/Placeholder.pdf")
    page_price = reader.pages[0]

    page_base.merge_page(page_price)

    writer = PyPDF2.PdfWriter()
    writer.add_page(page_base)
    with open(path, "wb") as fp:
        writer.write(fp)

if __name__ == '__main__':
    sti = "C:/Users/MMZ/Desktop/Alma Paldan O'Brien - 3k - inkl. pris.pdf"
    sti2 = "C:/Users/MMZ/Desktop/Asta Keogan Schlottmann - 3d.pdf"

    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    folder_path = filedialog.askdirectory()

    if folder_path == "":
        print("No folder was selected")

    pdf_file_path = sti2

    bp = get_booksprice(get_PDFreceipt_text(pdf_file_path))

    prices = []

    for book, price in bp:
        if price == None:
            price = lookup_price(book)
        prices.append(price)

    write_prices_pdf(pdf_file_path, prices)
