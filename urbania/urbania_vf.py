import traceback
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
options.add_argument(f'user-agent={random.choice(user_agents)}')
options.add_argument('--disable-extensions')
service = webdriver.ChromeService(executable_path='chromedriver.exe')
#service = webdriver.ChromeService('./chromedriver')

input_csv = './urbania/urbania_links.csv'
df = pd.read_csv(input_csv)
resultados = []

# Iterar sobre cada fila del CSV
#for index, row in df.iterrows(): 
for index, row in df.head(3).iterrows():
    link = row['Link']
    distrito = row['Dirección']

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 100)

    driver.get(link)

    # Esperar a que el botón de cookies aparezca y hacer clic
    cookies = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cookies-policy"]/div/div/div[2]/button'))) 
    cookies.click()

    try:
        direccion_element = driver.find_element(By.CSS_SELECTOR, 'h4#ref-map')
        direccion = direccion_element.text.strip()
    except Exception as e:
        direccion = "No especificada"

    try:
        estado = driver.find_element(By.CSS_SELECTOR, 'div.status-delivery')
        etapa = estado.find_element(By.CSS_SELECTOR, 'div.IN_PROGRESS').text[:-2]
    except Exception as e:
        etapa = "sin estado"

    try:
        fecha_entrega = driver.find_element(By.XPATH,'//*[@id="article-container"]/div[1]/div/span[2]').text
    except Exception as e:
        fecha_entrega = "sin fecha_entrega"

    try:
        # Extraer las áreas comunes
        areas_comunes_box = driver.find_element(By.ID, 'reactGeneralFeatures')
        areas_comunes_elements = areas_comunes_box.find_elements(By.XPATH, './div/div')
        areas_comunes = [element.text.strip() for element in areas_comunes_elements]
    except Exception as e:
        areas_comunes = []

    try:
        # Extraer el texto del XPath dado
        referencia = driver.find_element(By.XPATH, '//*[@id="new-gallery-portal"]/div/div[2]/div/div').text
    except Exception as e:
        referencia = "sin referencia"

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
            latitud = "sin latitud"
            longitud = "sin longitud"
    except Exception as e:
        latitud = "sin latitud"
        longitud = "sin longitud"

    try:
        # Extraer el elemento del mapa estático
        unidades_box = driver.find_element(By.ID, 'reactDevelopmentUnits')
        unidades_nav = unidades_box.find_element(By.CSS_SELECTOR, 'div.selectorsContainer')
        botones = unidades_nav.find_elements(By.XPATH, './button')

        for i in range(len(botones)):
            
            botones = unidades_nav.find_elements(By.XPATH, './button')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(botones[i]))
            botones[i].click()

            departamentos_box = unidades_box.find_element(By.CSS_SELECTOR, 'div.unitsContainerVertical')
            departamentos_list = departamentos_box.find_element(By.CSS_SELECTOR, 'div.flickity-slider')
            departamentos = departamentos_list.find_elements(By.XPATH, './div')

            for departamento in departamentos:

                #detalles_box = departamento.find_element(By.CSS_SELECTOR, 'div.unitFeatures')
                #metros = detalles_box.find_element(By.XPATH, './span[1]')
                #metros_txt = metros.get_attribute('innerHTML')

                a_element = departamento.find_element(By.CSS_SELECTOR, 'a')
                url = a_element.get_attribute('href')
                
                service2 = webdriver.ChromeService(executable_path='chromedriver2.exe')
                driveraux = webdriver.Chrome(service=service2, options=options)
                driveraux.get(url)

                precio = driveraux.find_element(By.CSS_SELECTOR,'div.price-items')

                caracteristicas = driveraux.find_element(By.CSS_SELECTOR, 'div.development-features-grid')

                area = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-stotal")]]')
                baño = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-bano")]]')
                dormitorios = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-dormitorio")]]')
                mediobaño = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-toilete")]]')

                print(precio.text)
                
                driveraux.quit()
                    



        
    except Exception as e:
        print(traceback.format_exc())

    # Agregar los resultados

    #resultados.append((link, direccion, estado_final, direccion, fecha_entrega,', '.join(areas_comunes),referencia,latitud,longitud))
    resultados.append((link,referencia,latitud,longitud,direccion,distrito,etapa,fecha_entrega,'financiamiento',areas_comunes))
    
    driver.quit()


output_csv = './urbania/urbania_vf.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['link', 'referencia', 'latitud', 'longitud', 'direccion','distrito','etapa','fecha_entrega','areas_comunes'])
    csvwriter.writerows(resultados)
