import os
import PyPDF2
import re
from fpdf import FPDF
import tkinter
from tkinter import filedialog

def get_booksprice(filepath:str):
    """
    params: A string of text that has been extracted from a pdf receipt
    returns: A list of book title and price pairs. If the price is not in the file, the price is set to None
    """
    text = get_PDFreceipt_text(filepath)

    spliton1 = 'rykker'
    spliton2 = 'ved gennemgang af bibliotekets udlån kan vi se'

    if has_price(text, filepath):
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

def has_price(text:str, filepath)-> bool:
    """
    params:  A text extracted from a PDF receipt
    returns: A bool on whether the receipt contains a price
    """
    if "rykker" in text:
        print(f'The book(s) in the file: \"{filepath}\" does not have a price\n')
        return False
    elif "pris" in text:
        print(f'The book(s) in the file: \"{filepath}\" has a price\n')
        return True
    else:
        print(f'unable to determine if the books in the file: \"{filepath}\" have a price\n')
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
    with open("ghg books/bookprices.txt", encoding='utf-8') as file:
        lines = [line.rstrip() for line in file]
    for bp in lines:
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
    with open("ghg books/bookprices.txt", "a", encoding='utf-8') as fileobj:
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
        p = str(p)
        pdf.cell(ln=0, h=5.0, align='L', w=0, txt=p, border=0)
        y+=4
    
    pdf.output('ghg books/Placeholder.pdf', 'F')
    
    reader = PyPDF2.PdfReader("ghg books/Placeholder.pdf")
    page_price = reader.pages[0]

    page_base.merge_page(page_price)

    writer = PyPDF2.PdfWriter()
    writer.add_page(page_base)

    try:
        with open(path, "wb") as fp:
            writer.write(fp)
    except PermissionError:
        print(f"The programme does not have permission to write in the file \"{path}\". Please make sure that the file is not open in other programmes.")

if __name__ == '__main__':
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    folder_path = filedialog.askdirectory()

    if folder_path == "":
        print("No folder was selected")
        exit()

    dir_list = os.listdir(folder_path)
    
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            filepath = os.path.join(folder_path, file)

            bp = get_booksprice(filepath)
            prices = []

            for book, price in bp:
                if price == None:
                    price = lookup_price(book)
                prices.append(price)

            write_prices_pdf(filepath, prices)
