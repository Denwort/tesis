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

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 100)

with open('nexoinmobiliaria.csv', 'r', encoding='utf-8') as csvfile:
    lines = csvfile.readlines()
    for line in lines[1:]:
        row = line.strip().split(",", 1)
        resultados.append((row[0], row[1]))

        link = row[0]        
        driver.get(link)
        direccion = wait.until(EC.presence_of_element_located((By.ID, "search-projects-normales"))) 


print(len(resultados))

'''

driver.get(f"https://nexoinmobiliario.pe/busqueda/venta-de-departamentos")
listado = wait.until(EC.presence_of_element_located((By.ID, "search-projects-normales"))) 

ofertas = listado.find_elements(By.XPATH, './article')

for oferta in ofertas:
    direccion = oferta.find_element(By.XPATH, './div[2]/div/div[2]/div/h3').text
    link = oferta.find_element(By.XPATH, './/div[contains(@class, "spld__profile")]/a').get_attribute('href')
    print(direccion, link)
    resultados.append((link, direccion))

driver.quit()

'''