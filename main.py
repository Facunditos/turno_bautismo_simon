import requests 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# Configurar la ruta del driver
service = Service('/usr/bin/chromedriver')

driver = webdriver.Chrome(options=chrome_options)
try:
    url = f"https://www.natividad.org.ar/turnos_bautismo.php"
    # Abrir la página web
    driver.get(url)
    # Esperar hasta que los comentarios estén visibles en la página
    tag_name_center = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "center"))
    )
    texto_tag_name_center = tag_name_center.text
    msg_sin_turnos = 'En este momento la parroquia no cuenta con cupos para bautismos.\nDisculpe las molestias.'
    if texto_tag_name_center != msg_sin_turnos :
          print('mandar whatsapp porque el texto central no indica falta de cupo')
    else:
          print('volver a probar en una hora')          
          
except:
    print("mandar whatsapp porque no se sabe el motivo por el cual la página no funciona")
    # Cerrar el navegador
    driver.quit()    
