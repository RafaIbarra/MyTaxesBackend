import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import HttpResponse
from django.shortcuts import render

class ScrapingView(APIView):
    def get(self, request, *args, **kwargs):
        url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id=01800319702001005008254822024103013609116639&dFeEmiDE=323032342d31302d33305430303a30303a3030&dRucRec=80022259&dTotGralOpe=591000&dTotIVA=53727&cItems=3&DigestValue=7838303173777a3855384e496d6b526d6b314c6a6d5070656a5551354c4445566273764c736d697a2f36553d&IdCSC=1&cHashQR=4b5c56ba7b9a253567c30e96621f744227cd7178a39650f24dbd9db57f05e4d5"  # URL del sitio web a scrapear
        url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id=01800319702001005008254822024103013609116639&dFeEmiDE=323032342d31302d33305430303a30303a3030&dRucRec=80022259&dTotGralOpe=591000&dTotIVA=53727&cItems=3&DigestValue=7838303173777a3855384e496d6b526d6b314c6a6d5070656a5551354c4445566273764c736d697a2f36553d&IdCSC=1&cHashQR=4b5c56ba7b9a253567c30e96621f744227cd7178a39650f24dbd9db57f05e4d5"
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            return Response({"error": "No se pudo acceder al sitio web"}, status=status.HTTP_400_BAD_REQUEST)

        # Parsear el contenido de la página
        soup = BeautifulSoup(response.content, "html.parser")
        consulta_form = soup.find("fieldset", id="consultaform")
        print(consulta_form)
        noticias = []
        
        # Extraer información específica (esto dependerá de la estructura HTML del sitio)
        # for articulo in soup.select(".noticia"):
        #     titulo = articulo.select_one(".titulo").get_text(strip=True)
        #     resumen = articulo.select_one(".resumen").get_text(strip=True)
        #     link = articulo.select_one("a")["href"]

        #     noticias.append({
        #         "titulo": titulo,
        #         "resumen": resumen,
        #         "link": link,
        #     })


        return Response(noticias, status=status.HTTP_200_OK)
    

# class ScrapingViewSelenium(APIView):
#     def get(self, request, *args, **kwargs):
#         driver = webdriver.Chrome()  # Asegúrate de tener ChromeDriver instalado
#         url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id=01800319702001005008254822024103013609116639&dFeEmiDE=323032342d31302d33305430303a30303a3030&dRucRec=80022259&dTotGralOpe=591000&dTotIVA=53727&cItems=3&DigestValue=7838303173777a3855384e496d6b526d6b314c6a6d5070656a5551354c4445566273764c736d697a2f36553d&IdCSC=1&cHashQR=4b5c56ba7b9a253567c30e96621f744227cd7178a39650f24dbd9db57f05e4d5"  # URL del sitio web a scrapear
#         # Abrir la página
#         driver.get(url)  # Cambia a la URL de la página real

#         # Esperar a que el fieldset con id="consultaform" esté presente
#         try:
#             consulta_form = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "consultaform"))
#             )

#             # Extraer y procesar los datos dentro del fieldset
#             # Ejemplo: obtener el texto de todos los párrafos dentro del fieldset
#             for p in consulta_form.find_elements(By.TAG_NAME, "p"):
#                 print(p.text)

#             # Ejemplo: obtener el valor de todos los inputs dentro del fieldset
#             for input_element in consulta_form.find_elements(By.TAG_NAME, "input"):
#                 print(f"{input_element.get_attribute('name')}: {input_element.get_attribute('value')}")

#         finally:
#             driver.quit()

#         return Response({'datos'}, status=status.HTTP_200_OK)

class ScrapingViewSelenium(APIView):
    def post(self, request, *args, **kwargs):
        # Configuración de opciones para el modo headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Habilitar modo headless
        chrome_options.add_argument("--no-sandbox")  # Opciones recomendadas
        chrome_options.add_argument("--disable-dev-shm-usage")  # Opciones recomendadas

        # Inicializar el servicio de ChromeDriver
        service = Service('path/to/chromedriver')  # Cambia 'path/to/chromedriver' a la ubicación de tu ChromeDriver
        driver = webdriver.Chrome( options=chrome_options)

        # url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id=01800319702001005008254822024103013609116639&dFeEmiDE=323032342d31302d33305430303a30303a3030&dRucRec=80022259&dTotGralOpe=591000&dTotIVA=53727&cItems=3&DigestValue=7838303173777a3855384e496d6b526d6b314c6a6d5070656a5551354c4445566273764c736d697a2f36553d&IdCSC=1&cHashQR=4b5c56ba7b9a253567c30e96621f744227cd7178a39650f24dbd9db57f05e4d5"  # URL del sitio web a scrapear
        url = request.data.get('url')
        if not url:
            return Response({'error': 'La URL es requerida.'}, status=status.HTTP_400_BAD_REQUEST)

        # Abrir la página
        driver.get(url)

        # Esperar a que el fieldset con id="consultaform" esté presente
        try:
            consulta_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "consultaform"))
            )

            # Extraer y procesar los datos dentro del fieldset
            datos = {}
            # Obtener el texto de todos los párrafos dentro del fieldset
            for p in consulta_form.find_elements(By.TAG_NAME, "p"):
                print(p.text)

            # Obtener el valor de todos los inputs dentro del fieldset
            for input_element in consulta_form.find_elements(By.TAG_NAME, "input"):
                datos[input_element.get_attribute('name')] = input_element.get_attribute('value')

            print(datos)
            respuesta={
                'datos':datos,
                'url':url

            }

        finally:
            driver.quit()

        return Response(respuesta, status=status.HTTP_200_OK)
    

class Home(APIView):
    
    
    def get(self, request, *args, **kwargs):
        # html_content = "<html><body><h1>Bienvenido</h1></body></html>"
        # # return Response('Bienvenido', status=status.HTTP_200_OK)
        # return Response(html_content, status=status.HTTP_200_OK, content_type="text/html")
    
        # html_content = "<html><body><h1>Bienvenido</h1></body></html>"
        html = render(request, 'home2.html')
        return HttpResponse(html, status=status.HTTP_200_OK, content_type="text/html")