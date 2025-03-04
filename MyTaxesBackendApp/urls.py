from django.urls import path
from MyTaxesBackendApp.scraping import *
from MyTaxesBackendApp.views import *
from MyTaxesBackendApp.Apis.Registros.Usuarios import *
from MyTaxesBackendApp.Apis.Registros.Operaciones import *
from MyTaxesBackendApp.Apis.Listados.ListadosRegistro import *
from MyTaxesBackendApp.Apis.Utilidades.Api_Utilidades import *
from MyTaxesBackendApp.Apis.Registros.RegistroVersiones import *
urlpatterns = [
    path('ScrapingDatos/',ScrapingDatos,name='ScrapingDatos'),
    path("scraping/", ScrapingView.as_view(), name="scraping"),
    path("scrapingselenium/", ScrapingViewSelenium.as_view(), name="ScrapingViewSelenium"),
    path("LecturaArchivoXml/", LecturaArchivoXml.as_view(), name="LecturaArchivoXml"),
    path('RegistroUsuario/',RegistroUsuario.as_view(),name="RegistroUsuario"), 
    path('RegistroVersion/',RegistroVersion.as_view(),name="RegistroVersion"), 
    path('ComprobarVersion/',ComprobarVersion.as_view(),name="ComprobarVersion"), 
    path('EliminarSesiones/',EliminarSesiones.as_view(),name="EliminarSesiones"), 
    path('Login/',Login.as_view(),name="Login"), 
    path('ComprobarSesionUsuario/',comprobarsesionusuario,name="comprobarsesionusuario"), 
    path('RegistroFactura/',registrofactura,name="registrofactura"), 
    path('EliminarFactura/',eliminarfactura,name="eliminarfactura"), 
    path('MovimientosFacturas/<int:anno>/<int:mes>/<int:id>/',MovimientosFacturas,name="MovimientosFacturas"), 
    path('ResumenPeriodo/<int:anno>/',ResumenPeriodo,name="ResumenPeriodo"), 

    path('UploadAudio/',upload_audio,name="upload_audio"), 
    path('prueba_transcripcion/',prueba_transcripcion,name="prueba_transcripcion"), 

     path('Meses/',meses,name='meses'),

     path('GenerarArchivoCsv/<int:anno>/<int:mes>/',GenerarArchivoCsv,name="GenerarArchivoCsv"), 

     path('RegistroMeses/',registromeses,name='registromeses'),

     path('ListaEmpresas/',ListaEmpresas,name='ListaEmpresas'),

     path('ConsultaArchivosXML/',ConsultaArchivosXML,name='ConsultaArchivosXML'),

     path('SolicitudRecuperacionContraseña/',SolicitudRecuperacionContraseña.as_view(),name='SolicitudRecuperacionContraseña'),
     path('ActualizacionPassword/',ActualizacionPassword.as_view(),name='ActualizacionPassword'),
     path('ComprobarCodigoSeguridad/',ComprobarCodigoSeguridad.as_view(),name='ComprobarCodigoSeguridad'),




    
    
]

