# Introduction
This Project aims to simplify inventory management of consumables(Hopfenkracherl) for the "Hochspannungszeichensaal TU Graz".

# Setup
```
pip install pdfplumber
```
Grant you Inventory file full permission (close all instances of the file!).
Windows Powershell:
```
icacls "Inventory.csv" /grant Everyone:F
```

# Functions

## GetCurrentInventory
