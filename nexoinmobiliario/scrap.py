from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import csv
import time
import random
import traceback

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]
options = webdriver.ChromeOptions()
options.add_argument('--disable-javascript')
options.add_argument(f'user-agent={random.choice(user_agents)}')
options.add_argument('--disable-extensions')
#options.add_argument('--headless') # No muestra la ventana
service = webdriver.ChromeService(executable_path='chromedriver.exe')

resultados = []

driver = webdriver.Chrome(service=service, options=options)

def check_element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except Exception:
        return False

with open('./nexoinmobiliario/links.csv', 'r', encoding='utf-8') as csvfile:
    lines = csvfile.readlines()

    for line in lines[1:]:
        row = line.strip().split(",", 1)

        link = row[0]        
        driver.get(link)
        
        try:

            header = driver.find_element(By.XPATH, '//*[@id="cont_ficha_desktop"]/article/header')
            referencia = header.find_element(By.XPATH, './div[1]/h1').text
            direccion = header.find_element(By.XPATH, './div[1]/p[1]').text 
            location = header.find_element(By.XPATH, './div[1]/p[2]').text
            direccion_parts = location.split("- ")
            distrito = direccion_parts[1] if len(direccion_parts) > 1 else location
            latitud = driver.find_element(By.ID, 'latitude').get_attribute('value')
            longitud = driver.find_element(By.ID, 'longitude').get_attribute('value')

            informacion = driver.find_element(By.XPATH, '//*[@id="cuadro_fix"]/div/table')
            etapa = informacion.find_element(By.XPATH, './tbody/tr[4]/td[2]').text
            fecha_entrega = informacion.find_element(By.XPATH, './tbody/tr[5]/td[2]').text
            financiamiento = informacion.find_element(By.XPATH, './tbody/tr[6]/td[2]').text

            ul_exists = check_element_exists(driver, By.CSS_SELECTOR, 'ul.Project-areas-list')
            areas_comunes = []
            if ul_exists:
                ul = driver.find_element(By.CSS_SELECTOR, 'ul.Project-areas-list')
                li = ul.find_elements(By.TAG_NAME, 'li')
                areas_comunes = [li.text for li in li]

            nav_flat_exists = check_element_exists(driver, By.ID, 'nav-flat')
            nav_duplex_exists = check_element_exists(driver, By.ID, 'nav-duplex')

            if nav_flat_exists:

                flat_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#nav-flat"]')
                flat_tab.click()

                nav_flat = driver.find_element(By.ID, 'nav-flat')
                flats = nav_flat.find_elements(By.CLASS_NAME, 'Project-available-model')

                for flat in flats:
                    
                    tipo = "flat"
                    tipologia = flat.find_element(By.XPATH, './/span[contains(@class, "name_tipology")]').text
                    pisos = flat.find_element(By.CSS_SELECTOR, 'span.num_pisos').text
                    dormitorios = flat.find_element(By.CSS_SELECTOR, 'span.bedroom').text
                    area = flat.find_element(By.CSS_SELECTOR, 'span.area').text
                    precio = flat.find_element(By.CSS_SELECTOR, 'span.price').text

                    resultados.append((link, referencia, latitud, longitud, direccion, distrito, etapa, fecha_entrega, financiamiento, areas_comunes, tipo, tipologia, pisos, dormitorios, area, precio))

            if nav_duplex_exists:

                duplex_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#nav-duplex"]')
                duplex_tab.click()

                nav_duplex = driver.find_element(By.ID, 'nav-duplex')
                flats = nav_duplex.find_elements(By.CLASS_NAME, 'Project-available-model')

                for flat in flats:
                    
                    tipo = "duplex"
                    tipologia = flat.find_element(By.CSS_SELECTOR, 'span.name_tipology').text
                    pisos = flat.find_element(By.CSS_SELECTOR, 'span.num_pisos').text
                    dormitorios = flat.find_element(By.CSS_SELECTOR, 'span.bedroom').text
                    area = flat.find_element(By.CSS_SELECTOR, 'span.area').text
                    precio = flat.find_element(By.CSS_SELECTOR, 'span.price').text

                    resultados.append((link, referencia, latitud, longitud, direccion, distrito, etapa, fecha_entrega, financiamiento, areas_comunes, tipo, tipologia, pisos, dormitorios, area, precio))

            if nav_flat_exists == False and nav_duplex_exists == False:
                print(f"{link}")

        except Exception as e:
            print(f"{link}")
            #print(traceback.format_exc()) 
        
with open('./nexoinmobiliario/scrap.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['link', 'referencia', 'latitud', 'longitud', 'direccion', 'distrito', 'etapa', 'fecha_entrega', 'financiamiento', 'areas_comunes', 'tipo', 'tipologia', 'piso', 'dormitorios', 'area', 'precio'])
    csvwriter.writerows(resultados)

driver.quit()

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