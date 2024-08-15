from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options

from ReadBills import read_csv, overwrite_cell

def get_inventory(content):

    # Set up Firefox options to run in headless mode
    fireoptions = Options()
    fireoptions.add_argument("--headless")

    driver = webdriver.Firefox(options = fireoptions)
    driver.get("http://" + content[2] + "/bks-web/login.php")

    # Handle login
    elem = driver.find_element(By.NAME, "user")
    elem.clear()
    elem.send_keys(content[0])
    elem = driver.find_element(By.NAME, "pwd")
    elem.clear()
    elem.send_keys(content[1])
    elem = driver.find_element(By.NAME, "submit")
    elem.click()

    # Go to product list
    driver.get("http://" + content[2] + "/bks-web/produktliste.php")

    # Find product in database and update csv
    csv_content = read_csv('Inventory.csv')

    print("working...")

    for index, product in enumerate(csv_content):
        for tr_index in range(4, len(driver.find_elements(By.TAG_NAME, 'tr'))): # Product contents start at 4
            if product[3] == driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[1]").text: #matching pid
                
                # Product found
                print(product[0])
                elem = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[4]").text #obtain the stock
                overwrite_cell('Inventory.csv', index, 2, elem) # Update the csv file
                break

    driver.close()
    print("finished!")