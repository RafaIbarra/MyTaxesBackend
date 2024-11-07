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
import xml.etree.ElementTree as ET 

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
            # for p in consulta_form.find_elements(By.TAG_NAME, "p"):
            #     print(p.text)

            # Obtener el valor de todos los inputs dentro del fieldset
            for input_element in consulta_form.find_elements(By.TAG_NAME, "input"):
                datos[input_element.get_attribute('name')] = input_element.get_attribute('value')

            
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
    



class LecturaArchivoXml(APIView):
    def post(self, request, *args, **kwargs):
        # Configuración de opciones para el modo headless
        xml_file = request.FILES['file']
        namespace = {'sifen': 'http://ekuatia.set.gov.py/sifen/xsd'}
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Acceder a los elementos usando el prefijo del espacio de nombres
            de_element = root.find('sifen:DE', namespace)
            # if de_element is not None:
            #     print("Elemento DE encontrado:", de_element.attrib)
            # else:
            #     print("Elemento DE no encontrado")

            # Ejemplo para acceder a un elemento dentro de <DE>
            NroRuc=''
            dig_ver=''
            Ruc_empresa=''
            nombre_empres=''

            dv_element = root.find('.//sifen:dRucEm', namespace)
            if dv_element is not None:
                NroRuc= dv_element.text
            else:
                NroRuc="No encontrado"

            dv_element = root.find('.//sifen:dDVEmi', namespace)
            if dv_element is not None:
                dig_ver= dv_element.text
            else:
                dig_ver="No encontrado"

            

            dv_element = root.find('.//sifen:dNomEmi', namespace)
            if dv_element is not None:
                nombre_empres= dv_element.text
            else:
                nombre_empres="No encontrado"

            Ruc_empresa=NroRuc + '-' + dig_ver
            data_empresa={
                'NroRuc':Ruc_empresa,
                'Empresa':nombre_empres

            }

            fechafac=''
            establecimiento=''
            punto_exp=''
            nro_doc =''
            timbrado=''
            
            dv_element = root.find('.//sifen:dFeEmiDE', namespace)
            if dv_element is not None:
                fechafac= dv_element.text
            else:
                fechafac="No encontrado"

            dv_element = root.find('.//sifen:dEst', namespace)
            if dv_element is not None:
                establecimiento= dv_element.text
            else:
                establecimiento="No encontrado"

            dv_element = root.find('.//sifen:dPunExp', namespace)
            if dv_element is not None:
                punto_exp= dv_element.text
            else:
                punto_exp="No encontrado"

            dv_element = root.find('.//sifen:dNumDoc', namespace)
            if dv_element is not None:
                nro_doc= dv_element.text
            else:
                nro_doc="No encontrado"

            nro_factura=establecimiento + '-'+punto_exp + '-'+nro_doc

            dv_element = root.find('.//sifen:dNumTim', namespace)
            if dv_element is not None:
                timbrado= dv_element.text
            else:
                timbrado="No encontrado"


            data_factura={
                'FechaOperacion':fechafac,
                'NroFactura':nro_factura,
                'Timbrado': timbrado
            }

            items_data = []
            conceptos = {}
            v_element = root.find('.//sifen:gCamItem', namespace)
            print(v_element)
            # Recorrer cada <gCamItem> en el XML
            for i, item in enumerate(root.findall('.//sifen:gCamItem', namespace), start=1):
                # Extraer los datos deseados y guardarlos en un diccionario
                item_data = {
                    "dCodInt": item.find('sifen:dCodInt', namespace).text,
                    "dDesProSer": item.find('sifen:dDesProSer', namespace).text,
                    "dDesUniMed": item.find('sifen:dDesUniMed', namespace).text,
                    "dCantProSer": item.find('sifen:dCantProSer', namespace).text,
                    "dPUniProSer": item.find('sifen:gValorItem/sifen:dPUniProSer', namespace).text,
                    "dTotBruOpeItem": item.find('sifen:gValorItem/sifen:dTotBruOpeItem', namespace).text,
                    "dDescItem": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dDescItem', namespace).text,
                    "dPorcDesIt": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dPorcDesIt', namespace).text,
                    "dDescGloItem": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dDescGloItem', namespace).text,
                    "dAntPreUniIt": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dAntPreUniIt', namespace).text,
                    "dAntGloPreUniIt": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dAntGloPreUniIt', namespace).text,
                    "dTotOpeItem": item.find('sifen:gValorItem/sifen:gValorRestaItem/sifen:dTotOpeItem', namespace).text,
                    "iAfecIVA": item.find('sifen:gCamIVA/sifen:iAfecIVA', namespace).text,
                    "dDesAfecIVA": item.find('sifen:gCamIVA/sifen:dDesAfecIVA', namespace).text,
                    "dPropIVA": item.find('sifen:gCamIVA/sifen:dPropIVA', namespace).text,
                    "dTasaIVA": item.find('sifen:gCamIVA/sifen:dTasaIVA', namespace).text,
                    "dBasGravIVA": item.find('sifen:gCamIVA/sifen:dBasGravIVA', namespace).text,
                    "dLiqIVAItem": item.find('sifen:gCamIVA/sifen:dLiqIVAItem', namespace).text,
                    "dBasExe": item.find('sifen:gCamIVA/sifen:dBasExe', namespace).text
                }
                
                # Agregar el diccionario a la lista
                items_data.append(item_data)
                conceptos[f"Item_{i}"] = item_data

            # Mostrar los datos extraídos

            NroRuc_cliente=''
            dig_ver_cliente=''
            Ruc_empresa_cliente=''
            nombre_cliente=''

            dv_element = root.find('.//sifen:dRucRec', namespace)
            if dv_element is not None:
                NroRuc_cliente= dv_element.text
            else:
                NroRuc_cliente="No encontrado"

            dv_element = root.find('.//sifen:dDVRec', namespace)
            if dv_element is not None:
                dig_ver_cliente= dv_element.text
            else:
                dig_ver_cliente="No encontrado"

            Ruc_empresa_cliente=NroRuc_cliente + '-' + dig_ver_cliente

            dv_element = root.find('.//sifen:dNomRec', namespace)
            if dv_element is not None:
                nombre_cliente= dv_element.text
            else:
                nombre_cliente="No encontrado"

            data_cliente={
                'NroRuc':Ruc_empresa_cliente,
                'Empresa':nombre_cliente

            }
                        
            data={
                'DataEmpresa':data_empresa,
                'DataFactura':data_factura,
                'Conceptos':conceptos,
                'DataCliente':data_cliente
            }
            


            # Devolver el valor en la respuesta
            return Response(data, status=status.HTTP_200_OK)
            # print(data)
        except ET.ParseError:
                return Response({"error": "El archivo no es un XML válido"}, status=status.HTTP_400_BAD_REQUEST)

                

        