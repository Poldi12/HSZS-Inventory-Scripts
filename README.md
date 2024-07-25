# Introduction
This Project aims to simplify inventory management of consumables(Hopfenkracherl) for the "Hochspannungszeichensaal" at TU Graz.

# Setup
python 3.10
pip 24.1.2
```
pip install pdfplumber
```

Generate a folder named "Bills" in the same directory as the scripts.
Obtain the "Inventory.csv" file and place it also in the same directory as the scripts.

Grant you Inventory file full permission (close all instances of the file!).
Windows Powershell:
```
icacls "Inventory.csv" /grant Everyone:F
```

# Functions

## GetCurrentInventory

## ReadBills
Parses all .pdf files in "Bills/" directory, gets the amount of products, adds the "Bestand System" to it and saves it in "Bestan Real".
Also notices you, if it could not parse anything in the pdf or if it did not find the corresponding product in "Inventory.csv".