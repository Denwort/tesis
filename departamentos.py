from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from collections import defaultdict
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

contador = defaultdict(int)

for i in range(1, 767):

    print(i)

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 100)

    driver.get(f"https://urbania.pe/buscar/venta-de-departamentos?page={i}")
    cookies = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/button"))) 
    cookies.click()
    
    listado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "postings-container")))
    ofertas = listado.find_elements(By.XPATH, './div')

    for oferta in ofertas:
        direccion = oferta.find_element(By.XPATH, './/h2[starts-with(@class, "LocationLocation")]')
        distrito = direccion.text
        contador[distrito] += 1
        print(distrito)
    
    driver.quit()

    '''
    boton_siguiente_existe = driver.find_elements(By.XPATH, './/a[starts-with(@class, "PageArrow")]')
    if(boton_siguiente_existe):
        boton_siguiente = driver.find_element(By.XPATH, './/a[starts-with(@class, "PageArrow")]')
        time.sleep(random.uniform(5, 10))
        actions = ActionChains(driver)
        actions.move_to_element(boton_siguiente).click().perform()
        wait.until(EC.visibility_of_element_located((By.XPATH, './/div[starts-with(@class, "LoadingContainer")]')))
        wait.until(EC.invisibility_of_element_located((By.XPATH, './/div[starts-with(@class, "LoadingContainer")]')))
    else:
        continuar = False
    '''

print(contador)




'''
contact = wait.until(EC.presence_of_element_located((By.XPATH, contact_path)))


contact.click()

message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]'
message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
message_box.send_keys('ON' + Keys.ENTER)

while(True):
    print("Escuchando")
    last_message_path = '//*[@id="main"]/div[2]/div/div[2]/div[last()]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
    last_message = wait.until(EC.presence_of_element_located((By.XPATH, last_message_path)))
    last_text = last_message.get_attribute('innerText')

    if(last_text in ["201", "209", "204"]):

        if(last_text == "201"):
            moovitapp_link = 'https://moovitapp.com/lima-1102/lines/201/774953/3475219/es'
            huarochiri_path = '//*[@id="stop-36868473-6"]' 

        elif(last_text == "209"):
            moovitapp_link = 'https://moovitapp.com/lima-1102/lines/209/8988024/3941826/es'
            huarochiri_path = '//*[@id="stop-36868473-7"]'
        
        elif(last_text == "204"):
            moovitapp_link = 'https://moovitapp.com/lima-1102/lines/204/8988027/3941829/es'
            huarochiri_path = '//*[@id="stop-45546062-14"]'
        
        driver.execute_script("window.open('');") 
        driver.switch_to.window(driver.window_handles[1]) 
        driver.get(moovitapp_link)
        
        try:
            huarochiri = wait.until(EC.presence_of_element_located((By.XPATH, huarochiri_path)))
            huarochiri.click()
        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            message_box.send_keys('Error en Huarochiri' + Keys.ENTER)
            continue
        
        try:
            proxima_llegada_path = huarochiri_path + '/div[2]/div[2]/span'
            proxima_llegada = wait.until(EC.presence_of_element_located((By.XPATH, proxima_llegada_path)))
            proxima_llegada_text = proxima_llegada.get_attribute('innerHTML')
        except:
            proxima_llegada_text = 'Error en proxima llegada'
        
        try:
            mas_llegada_path = huarochiri_path + '/div[1]/div[2]/span[2]'
            mas_llegada = wait.until(EC.presence_of_element_located((By.XPATH, mas_llegada_path)))
            mas_llegada_text = mas_llegada.get_attribute('innerHTML')
        except:
            mas_llegada_text = 'Error en mas llegada'
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        text = proxima_llegada_text + "     " + mas_llegada_text
        message_box.send_keys(text + Keys.ENTER)
    
    elif(last_text == "exit"):
        break

    else:
        time.sleep(1)

message_box.send_keys('OFF' + Keys.ENTER)
driver.close()
os.system('shutdown /s /t 0')

'''