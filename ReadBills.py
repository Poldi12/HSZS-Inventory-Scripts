import pdfplumber

from os import listdir
from os.path import isfile, join

import re
import csv
from dataclasses import dataclass

@dataclass
class ProductInfo:
    ID: str
    value: int

def read_pdf(file_path):
    # open the PDF file
    with pdfplumber.open(file_path) as pdf:
        text = ''
        # iterate through all the pages and extract the text
        for page in pdf.pages:
            text = text + '\n' + page.extract_text()
        return text

def read_csv(file_path):
    with open(file_path, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        rows = [row for row in reader] #list of lists (row(column)) 
    return rows

def write_csv(file_path, rows):
    """
    Writes the list of rows to the CSV file.
    
    :param file_path: The path to the CSV file.
    :param rows: A list of rows, where each row is a list of cell values.
    """
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(rows)

def overwrite_cell(file_path, row_index, col_index, new_value):
    # Read the current contents of the CSV file
    rows = read_csv(file_path)
    
    # Overwrite the specific cell
    if 0 <= row_index < len(rows) and 0 <= col_index < len(rows[row_index]):
        rows[row_index][col_index] = new_value
    else:
        raise IndexError("Row or column index out of range")
    
    # Write the modified contents back to the CSV file
    write_csv(file_path, rows)

def update_products_in_csv(extracted_product_list):
    csv_content = read_csv('Inventory.csv')
    
    for product in extracted_product_list:
        for index_r, row in enumerate(csv_content):
            if row[5] == str(product.ID): #product ids match
                overwrite_cell('Inventory.csv', index_r, 1, int(row[2]) + int(product.value)) # 1 is "Bestand Real"
                break
            elif(index_r == len(csv_content)-1): #product not found in csv file
                print("Product ID not in csv file: " + str(product.ID))

def extract_product(pdf_text):
    #delete irrelevant lines, which could mess with further string operations
    string_list = pdf_text.splitlines()
    del string_list[0:21] #overhead 1.page
    for index, line in enumerate(string_list):
        if 'Seite' in line:
            del string_list[index:index+10] #overhead n+1.page
        if 'Gebindezusammenstellung' in line: #does not work sometimes, so wie also use Art.Nr.
            del string_list[index:]
        if 'Art.Nr.' in line:
            del string_list[index-1:]

    #save product and quantity to a list
    extracted_product_list = []
    for index, line in enumerate(string_list):
        try:
            #keg beer is calculated different
            if line[0:5] == '10095':
                back_cut = re.split('KEG', line)
                number_beer = back_cut[0][len(back_cut[0])-3:]

                extracted_product_list.append(ProductInfo(line[0:5], number_beer))

            elif line[0:5].isdigit():
                front_cut = re.split('\/', line)
                back_cut = re.split('KI', front_cut[1])
                numbers = re.split('\ ', back_cut[0])
                amount = int(numbers[0]) * int(numbers[1])
                
                extracted_product_list.append(ProductInfo(line[0:5], amount))

        except IndexError:
            print(line[0:5] + " skipped")

    update_products_in_csv(extracted_product_list)


# main
'''
bill_dir = "Bills/"
only_files = [f for f in listdir(bill_dir) if isfile(join(bill_dir, f))]

for pdf in only_files:
    print(pdf)
    pdf_text = read_pdf('Bills/'+ pdf)
    extract_product(pdf_text)

input('Succsessful!')
'''