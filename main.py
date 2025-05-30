from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import  pywhatkit as kit
from datetime import datetime
from time import sleep
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
service = Service('/usr/bin/chromedriver')

mariana_num = os.environ["MARIANA_NUM"]
# Se arranca en -1 porque la primera búsqueda no cuenta. 
n_busqueda = -1

def enviar_msg(mensaje):
    while True:
        # Si hay un error se espera 30 segundos antes de volver a enviarlo
        try:
            #kit.sendwhatmsg(mariana_num, mensaje, hora, minuto+1)
            kit.sendwhatmsg_instantly(mariana_num,mensaje,wait_time=10,tab_close=True,close_time=5)
            print("Mensage programado exitosamente!")
            break
        except Exception as e:
            print(f"Ocurrió un error al enviar el mensaje: {e}. Se esperan 30 segundos para volver a intertarlo")
            sleep(30)

def buscar_turno():
    url = "https://www.natividad.org.ar/turnos_bautismo.php"
    # Abrir la página web
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        # Esperar hasta que los comentarios estén visibles en la página. Si el elemento no se encuenta, se ejecuta el bloque except
        tag_name_center = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "center"))
        )
        texto_tag_name_center = tag_name_center.text
        msg_sin_turnos = 'En este momento la parroquia no cuenta con cupos para bautismos.\nDisculpe las molestias.'
        if texto_tag_name_center != msg_sin_turnos :
            msg = f'Es muy probable que esté habilitada la reserva de turnos! \U0001F600\n{url}'
            for _ in range(2):
                enviar_msg(msg)
                sleep(30)
        else:
            marca_tiempo = str(datetime.now()).split('.')[0]
            print(f'hora actual: {marca_tiempo}. Volveremos a probar dentro de quince minutos')          
            global n_busqueda
            n_busqueda +=1
            if n_busqueda == 8: # Pasaron dos horas (15 min * 8) de ejecución del script 
                msg = 'No encontramos turnos para el bautismo de Simón. Lo seguiremos intentando! \U0001F4AA'
                enviar_msg(msg)
                n_busqueda = 0
                
    except Exception as e:
        msg = f'Por algún motivo no pudimos consultar la disponibilidad de turnos \U0001F914. Te recomendamos que visitas la página.\n{url}'
        for _ in range(2):
            enviar_msg(msg)
            sleep(30)
        print(f"Ocurrió un error al visitar la página: {e}.")
    
    # Cerrar el navegador
    driver.quit()    


def main():
    msg = 'Buen día Mariana! Hoy nos pondremos a buscar un turno para el bautismo de Simón. Crucemos los dedos! \U0001F91E'
    enviar_msg(msg)
    while True:
        buscar_turno()
        quince_minutos = 60 * 15
        sleep(quince_minutos)
        

main()        

