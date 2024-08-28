from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import random
import re

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]
options = webdriver.ChromeOptions()
options.add_argument('--disable-javascript')
options.add_argument(f'user-agent={random.choice(user_agents)}')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
#service = webdriver.ChromeService(executable_path='chromedriver.exe')
service = webdriver.ChromeService('./chromedriver')

input_csv = './urbania/urbania_links.csv'
df = pd.read_csv(input_csv)
resultados = []

# Iterar sobre cada fila del CSV
#for index, row in df.iterrows(): 
for index, row in df.head(3).iterrows():
    link = row['Link']
    direccion = row['Dirección']

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 100)

    driver.get(link)

    # Esperar a que el botón de cookies aparezca y hacer clic
    cookies = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cookies-policy"]/div/div/div[2]/button'))) 
    cookies.click()

    try:
        direccion_element = driver.find_element(By.CSS_SELECTOR, 'h4#ref-map')
        direccion_extraida = direccion_element.text.strip()
    except Exception as e:
        direccion_extraida = "No especificada"

    try:
        estado = driver.find_element(By.CSS_SELECTOR, 'div.status-delivery')
        estado_final = estado.find_element(By.CSS_SELECTOR, 'div.IN_PROGRESS').text
    except Exception as e:
        estado_final = "entrega inmediata"

    try:
        fecha_entrega = driver.find_element(By.XPATH,'//*[@id="article-container"]/div[1]/div/span[2]').text
    except Exception as e:
        fecha_entrega = "entrega inmediata"

    try:
        # Extraer las áreas comunes
        areas_comunes_elements = driver.find_elements(By.CSS_SELECTOR, 'div.sc-gcUDKN div.sc-la-DkbX')
        areas_comunes = [element.text.strip() for element in areas_comunes_elements]
    except Exception as e:
        areas_comunes = []

    try:
        # Extraer el texto del XPath dado
        referencia = driver.find_element(By.XPATH, '//*[@id="new-gallery-portal"]/div/div[2]/div/div').text
    except Exception as e:
        referencia = "No hay referencia"

    try:
        # Extraer el elemento del mapa estático
        static_map_element = driver.find_element(By.ID, 'static-map')
        src_attribute = static_map_element.get_attribute('src')
        
        # Extraer la latitud y longitud usando una expresión regular
        lat_long_match = re.search(r'center=([-0-9.]+),([-0-9.]+)', src_attribute)
        if lat_long_match:
            latitud = lat_long_match.group(1)
            longitud = lat_long_match.group(2)
        else:
            latitud = "No encontrada"
            longitud = "No encontrada"
    except Exception as e:
        latitud = "No encontrada"
        longitud = "No encontrada"

    # Agregar los resultados

    #resultados.append((link, direccion, estado_final, direccion_extraida, fecha_entrega,', '.join(areas_comunes),referencia,latitud,longitud))
    resultados.append((link, referencia,latitud,longitud,direccion_extraida,direccion,estado_final,fecha_entrega,', '.join(areas_comunes)))
    
    driver.quit()


output_csv = './urbania/urbania_vf.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['link', 'referencia', 'latitud', 'longitud', 'direccion','distrito','etapa','fecha_entrega','areas_comunes'])
    csvwriter.writerows(resultados)
