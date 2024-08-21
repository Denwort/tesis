from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import csv
import time
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]
options = webdriver.ChromeOptions()
options.add_argument('--disable-javascript')
options.add_argument(f'user-agent={random.choice(user_agents)}')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
service = webdriver.ChromeService(executable_path='chromedriver.exe')

resultados = []

for i in range(1, 5): # 1 al 766

    #print(i)

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 100)

    driver.get(f"https://urbania.pe/buscar/venta-de-departamentos?page={i}")

    cookies = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/button"))) 
    cookies.click()
    
    listado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "postings-container")))
    ofertas = listado.find_elements(By.XPATH, './div')

    for oferta in ofertas:

        link = oferta.find_element(By.XPATH, './/div[starts-with(@class, "PostingCardLayout")]').get_attribute('data-to-posting')
        
        resultados.append([link])
    
    driver.quit()

    #aca con cada uno de ese link debes hacerle webscrapping otra vez para revisar q hay en cada una de las paginas
    


with open('resultados1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Link'])
    csvwriter.writerows(resultados)

print("war is over")