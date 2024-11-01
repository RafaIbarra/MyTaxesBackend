from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

@api_view(['GET'])
def ScrapingDatos(request):
    url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id=01800319702001005008254822024103013609116639&dFeEmiDE=323032342d31302d33305430303a30303a3030&dRucRec=80022259&dTotGralOpe=591000&dTotIVA=53727&cItems=3&DigestValue=7838303173777a3855384e496d6b526d6b314c6a6d5070656a5551354c4445566273764c736d697a2f36553d&IdCSC=1&cHashQR=4b5c56ba7b9a253567c30e96621f744227cd7178a39650f24dbd9db57f05e4d5"  # URL del sitio web a scrapear
    response = request.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        return Response({"error": "No se pudo acceder al sitio web"}, status=status.HTTP_400_BAD_REQUEST)

    # Parsear el contenido de la página
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    # noticias = []

    # # Extraer información específica (esto dependerá de la estructura HTML del sitio)
    # for articulo in soup.select(".noticia"):
    #     titulo = articulo.select_one(".titulo").get_text(strip=True)
    #     resumen = articulo.select_one(".resumen").get_text(strip=True)
    #     link = articulo.select_one("a")["href"]

    #     noticias.append({
    #         "titulo": titulo,
    #         "resumen": resumen,
    #         "link": link,
    #     })

    return Response({'mensaje':'Ok'}, status=status.HTTP_200_OK)