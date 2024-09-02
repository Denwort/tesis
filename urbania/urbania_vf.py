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
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = webdriver.ChromeService(executable_path='chromedriver.exe')
#service = webdriver.ChromeService('./chromedriver')

input_csv = './urbania/urbania_links.csv'
df = pd.read_csv(input_csv)
resultados = []

def check_element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except Exception:
        return False

# Iterar sobre cada fila del CSV
#for index, row in df.iterrows(): 
for index, row in df.iloc[13:16].iterrows():
    link = row['Link']
    distrito = row['Dirección']

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 100)

    driver.get(link)

    cookies = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cookies-policy"]/div/div/div[2]/button'))) 
    cookies.click()

    aviso_finalizado = check_element_exists(driver, By.CSS_SELECTOR, 'div.offline-content')
    if aviso_finalizado:
        print("finalizado:", link)
        continue

    es_proyecto = check_element_exists(driver, By.ID, 'reactDevelopmentUnits')

    try:
        direccion_element = driver.find_element(By.CSS_SELECTOR, 'div.section-location-property')
        direccion_h4 = direccion_element.find_element(By.XPATH, './h4')
        direccion = direccion_element.text.strip()
    except Exception as e:
        direccion = ""
        print("sin direccion:", link)

    try:
        estado = driver.find_element(By.CSS_SELECTOR, 'div.status-delivery')
        etapa = estado.find_element(By.CSS_SELECTOR, 'div.IN_PROGRESS').text[:-2]
    except Exception as e:
        etapa = ""
        if(es_proyecto==True):
            print("sin etapa:", link)

    try:
        fecha_entrega = driver.find_element(By.XPATH,'//*[@id="article-container"]/div[1]/div/span[2]').text
    except Exception as e:
        fecha_entrega = ""
        if(es_proyecto==True):
            print("sin fecha_entrega:", link)

    try:
        areas_comunes_box = driver.find_element(By.ID, 'reactGeneralFeatures')
        areas_comunes_elements = areas_comunes_box.find_elements(By.XPATH, './div/div[1]/div')
        areas_comunes = [element.text.strip() for element in areas_comunes_elements]
        print(areas_comunes)
    except Exception as e:
        areas_comunes = []
        print("sin areas_comunes:", link)

    try:
        referencia = driver.find_element(By.XPATH, '//*[@id="new-gallery-portal"]/div/div[2]/div/div').text
    except Exception as e:
        referencia = ""
        print("sin referencia:", link)

    try:
        static_map_element = driver.find_element(By.ID, 'static-map')
        src_attribute = static_map_element.get_attribute('src')
        
        lat_long_match = re.search(r'center=([-0-9.]+),([-0-9.]+)', src_attribute)
        if lat_long_match:
            latitud = lat_long_match.group(1)
            longitud = lat_long_match.group(2)
        else:
            latitud = ""
            longitud = ""
            print(link)
    except Exception as e:
        latitud = ""
        longitud = ""
        print("sin coordenadas:", link)

    if es_proyecto:
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

            #for departamento in departamentos:
            for departamento in departamentos[:2]:

                #detalles_box = departamento.find_element(By.CSS_SELECTOR, 'div.unitFeatures')
                #metros = detalles_box.find_element(By.XPATH, './span[1]')
                #metros_txt = metros.get_attribute('innerHTML')

                a_element = departamento.find_element(By.CSS_SELECTOR, 'a')
                url = a_element.get_attribute('href')
                
                service2 = webdriver.ChromeService(executable_path='chromedriver2.exe')
                #service2 = webdriver.ChromeService('./chromedriver')
                driveraux = webdriver.Chrome(service=service2, options=options)
                driveraux.get(url)

                try:
                    precio = driveraux.find_element(By.CSS_SELECTOR,'div.price-items')
                except Exception as e:
                    precio = ''
                    print("sin precio:", url)

                caracteristicas = driveraux.find_element(By.CSS_SELECTOR, 'div.development-features-grid')

                try:
                    area1 = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-stotal")]]')
                    area=area1.text
                except Exception as e:
                    area = ''
                    print("sin area:", url)

                try:
                    bano1 = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-bano")]]')
                    banos=bano1.text
                except Exception as e:
                    banos = ''
                    print("sin banos:", url)

                try:
                    dormitorios1 = caracteristicas.find_element(By.XPATH, '//li[i[contains(@class, "icon-dormitorio")]]')
                    dormitorios=dormitorios1.text
                except Exception as e:
                    dormitorios = ''
                    print("sin dormitorios:", url)

                try:
                    long_description_element = driver.find_element(By.ID, 'longDescription')
                    long_description = long_description_element.text.lower()
                    
                    if 'duplex' in long_description:
                        tipo = 'duplex'
                    else:
                        tipo = 'flat'
                except Exception as e:
                    tipo = 'flat' 
                
                finally:
                    driveraux.quit()
                
    else:
        print("aviso unico: ", link)
        tipo = 'unico' 

    #resultados.append((link, direccion, estado_final, direccion, fecha_entrega,', '.join(areas_comunes),referencia,latitud,longitud))
    resultados.append((link,referencia,latitud,longitud,direccion,distrito,etapa,fecha_entrega,areas_comunes,tipo,dormitorios,banos,area,precio))
    
    driver.quit()


output_csv = './urbania/urbania_vf.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['link', 'referencia', 'latitud', 'longitud', 'direccion','distrito','etapa','fecha_entrega','areas_comunes','tipo','dormitorios','banos','area','precio'])
    csvwriter.writerows(resultados)
