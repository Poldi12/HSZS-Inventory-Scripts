# Introduction
This project aims to simplify inventory management of consumables(Hopfenkracherl) with the dedicated kitchenserver.

# Setup
python 3.10
pip 24.1.2
```
pip install pdfplumber
pip install selenium
```

Generate a folder named "Bills" in the same directory as the scripts.
Generate a "credentials.txt" file and place it in the same directory as the scripts. Credentials have to contain your username in the first row, your password in the second, the production server in the third(10.110.0.42) and the testserver in the fourth(10.110.5.71).
Obtain the "Inventory.csv" file and place it in the same directory as the scripts.

Grant you Inventory file full permission (close all instances of the file!).
Windows Powershell:
```
icacls "Inventory.csv" /grant Everyone:F
```
# Application

Executable versions can be found in the output/ folder.

# Functions

## GetCurrentInventory
Pulls the current Inventory number from the Server and writes them to Inventory.csv in the "Bestand System" column. Can take some time (few minutes).

## UpdateInventory
Updates every Product on the Server to the "Bestand Real" value of Inventory.csv. Can take some time (few minutes).

## ReadBills
Parses all .pdf files in "Bills/" directory, gets the amount of products, adds the "Bestand System" to it and saves it in "Bestan Real".
Also notices you, if it could not parse anything in the pdf or if it did not find the corresponding product in "Inventory.csv".

# Misc
"program": "${file}"
