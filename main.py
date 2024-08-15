# Main script and user input handling

import ReadBills, GetInventory, UpdateInventory, sys, os

# Check if all required files are present
if(not(os.path.exists("Bills/") and os.path.isfile("credentials.txt") and os.path.isfile("Inventory.csv"))):
        input("File(s) are missing, please check if there is a Bills folder, a credentials.txt file and an"
              "Inventory.csv file in your current directory\nPress any key to exit.")
        sys.exit()

resp = input("Production(p) or Testserver(t)?\n")

with open('credentials.txt', 'r') as file:
        content = file.readlines()

# User input handling server choice
if (resp == "p"):
        print("#################\nProduction Server\n#################")
elif(resp == "t"):
        del content[2] # Delete production server address from list
        print("###########\nTest Server\n###########")
else:
        print("Invalid input, program exiting...")
        sys.exit()
        
# User input handling action choice
while(1<2):

    resp = input("Read Bills(r), Get Inventory(g), Update Inventory(u), Help(h), Exit(e)?\n")

    match resp:
            case "r":
                    ReadBills.read_bills()
            case "g":
                    GetInventory.get_inventory(content)
            case "u":
                    UpdateInventory.update_inventory(content)
            case "h":
                    print("Help\n####\nRead Bills(r) adds all products fetched from pdfs in the Bills "
                          "folder, adds them to the values in the 3. row and saves them to the 2. row "
                          "of Inventory.csv.\n"
                          "Get Inventory(g) pulls the current values of inventory and writes them "
                          "to the 2. row in Inventory.csv.\n"
                          "Update Inventory(u) writes the values of the 2. row in Inventory.csv to the "
                          "Server.\n"
                          "Exit(e) exits the program.\n"
                          "For further information read the README file of the project in the repo.\n")
            case "e":
                    sys.exit()
