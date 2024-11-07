from django.urls import path
from MyTaxesBackendApp.scraping import *
from MyTaxesBackendApp.views import *
urlpatterns = [
    path('ScrapingDatos/',ScrapingDatos,name='ScrapingDatos'),
    path("scraping/", ScrapingView.as_view(), name="scraping"),
    path("scrapingselenium/", ScrapingViewSelenium.as_view(), name="ScrapingViewSelenium"),
    path("LecturaArchivoXml/", LecturaArchivoXml.as_view(), name="LecturaArchivoXml")
    
    
]