from selenium import webdriver
from selenium.webdriver.common.by import By

from ReadBills import read_csv, overwrite_cell

driver = webdriver.Firefox()
driver.get("http://10.110.0.42/bks-web/login.php")

#handle login
with open('credentials.txt', 'r') as file:
    content = file.readlines()

elem = driver.find_element(By.NAME, "user")
elem.clear()
elem.send_keys(content[0])
elem = driver.find_element(By.NAME, "pwd")
elem.clear()
elem.send_keys(content[1])
elem = driver.find_element(By.NAME, "submit")
elem.click()

#go to product list
driver.get("http://10.110.0.42/bks-web/produktliste.php")

#find product in database and update csv
csv_content = read_csv('Inventory.csv')

for index, product in enumerate(csv_content):
    for tr_index in range(4, len(driver.find_elements(By.TAG_NAME, 'tr'))): #product contents start at 4
        if product[3] == driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[1]").text: #matching pid
            elem = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[" + str(tr_index) + "]/td[4]").text #obtain the stock
            overwrite_cell('Inventory.csv', index, 2, elem) #update the csv file
            break

driver.close()