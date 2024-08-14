from selenium import webdriver
from selenium.webdriver.common.by import By

from ReadBills import read_csv, overwrite_cell

def update_inventory(content):
    with open('credentials.txt', 'r') as file:
        content = file.readlines()

    driver = webdriver.Firefox()
    driver.get("http://10.110.5.71/bks-web/login.php") #10.110.5.71 live: 10.110.0.42

    #handle login
    elem = driver.find_element(By.NAME, "user")
    elem.clear()
    elem.send_keys(content[0])
    elem = driver.find_element(By.NAME, "pwd")
    elem.clear()
    elem.send_keys(content[1])
    elem = driver.find_element(By.NAME, "submit")
    elem.click()

    #go to product list
    driver.get("http://10.110.5.71/bks-web/produktliste.php")

    #find product in database and update database
    csv_content = read_csv('Inventory.csv')

    for index, product in enumerate(csv_content):
        for tr_index in range(4, len(driver.find_elements(By.TAG_NAME, 'tr'))): #product contents start at 4
            if product[3] == driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[1]").text: #matching pid

                elem = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[11]/a") 
                elem.click()

                #editing menu
                elem = driver.find_element(By.NAME, "new_Bestand")
                elem.clear()
                elem.send_keys(product[1]) #change later to 1
                elem = driver.find_element(By.NAME, "save_all")
                elem.click() #save new value
                #go again back to product list
                driver.get("http://10.110.5.71/bks-web/produktliste.php")
                break

    driver.close()