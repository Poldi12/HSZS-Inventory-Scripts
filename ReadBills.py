import pdfplumber

from os import listdir
from os.path import isfile, join

import re
import csv

def read_pdf(file_path):
    # open the PDF file
    with pdfplumber.open(file_path) as pdf:
        text = ''
        # iterate through all the pages and extract the text
        for page in pdf.pages:
            text = text + '\n' + page.extract_text()
        return text

def read_csv(file_path):
    """
    Reads the CSV file and returns its contents as a list of rows.
    
    :param file_path: The path to the CSV file.
    :return: A list of rows, where each row is a list of cell values.
    """
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
    return rows

def write_csv(file_path, rows):
    """
    Writes the list of rows to the CSV file.
    
    :param file_path: The path to the CSV file.
    :param rows: A list of rows, where each row is a list of cell values.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def overwrite_cell(file_path, row_index, col_index, new_value):
    """
    Overwrites a specific cell in the CSV file with a new value.
    
    :param file_path: The path to the CSV file.
    :param row_index: The index of the row containing the cell to overwrite.
    :param col_index: The index of the column containing the cell to overwrite.
    :param new_value: The new value to write to the cell.
    """
    # Read the current contents of the CSV file
    rows = read_csv(file_path)
    
    # Overwrite the specific cell
    if 0 <= row_index < len(rows) and 0 <= col_index < len(rows[row_index]):
        rows[row_index][col_index] = new_value
    else:
        raise IndexError("Row or column index out of range")
    
    # Write the modified contents back to the CSV file
    write_csv(file_path, rows)

def extract_product(pdf_text):
    #delete irrelevant lines, which could mess with string operations below
    stringlist = pdf_text.splitlines()
    del stringlist[0:21] #overhead 1.page
    for index, line in enumerate(stringlist):
        if 'Seite' in line:
            del stringlist[index:index+10] #overhead n+1.page
        if 'Gebindezusammenstellung' in line: #does not work sometimes, so wie also use Art.Nr.
            del stringlist[index:]
        if 'Art.Nr.' in line:
            del stringlist[index-1:]
    print(stringlist)

    #get product and quantity
    for line in stringlist:
        try:
            #keg beer is calculated different
            if line[0:5] == '10095':
                backcut = re.split('KEG', line)
                numberbeer = backcut[0][len(backcut[0])-3:]
                print(numberbeer)

            elif line[0:4].isdigit():
                frontcut = re.split('\/', line)
                backcut = re.split('KI', frontcut[1])
                numbers = re.split('\ ', backcut[0])
                amount = int(numbers[0]) * int(numbers[1])
                print(amount)
        except IndexError:
            print(line[0:5] + " skipped")


# main
billdir = "Bills/"
onlyfiles = [f for f in listdir(billdir) if isfile(join(billdir, f))]

for pdf in onlyfiles:
    print(pdf)
    pdf_text = read_pdf('Bills/'+ pdf)
    extract_product(pdf_text)
