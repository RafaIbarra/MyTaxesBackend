from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from MyTaxesBackendApp.Apis.Seguridad.obtener_datos_token import*
from MyTaxesBackendApp.Apis.Seguridad.Validaciones import *
from .generacion_datos import *
from MyTaxesBackendApp.Serializadores.FacturasSerializers import *
from MyTaxesBackendApp.Serializadores.ResumenPeriodoSerializers import *
from MyTaxesBackendApp.Serializadores.MesesSerializers import *
from MyTaxesBackendApp.models import Usuarios
import time
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
@api_view(['POST'])
def MovimientosFacturas(request,anno,mes,id):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        
        lista_facturas=registros_facturas(id_user,anno,mes,id)
        
        # lista_egresos_unico = [elemento for elemento in lista_egresos if elemento.get('id') == id]
        
        if lista_facturas:
            
            result_serializer=FacturasSerializer(lista_facturas,many=True)
            
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def ResumenPeriodo(request,anno):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        
        data_resumen=resumen_periodo(id_user,anno)
        
        # lista_egresos_unico = [elemento for elemento in lista_egresos if elemento.get('id') == id]
        
        if data_resumen:
            
            result_serializer=ResumenPeriodoSerializers(data_resumen,many=True)
            
            return Response(result_serializer.data,status= status.HTTP_200_OK)
        else:
            return Response([],status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    


@api_view(['POST'])
def meses(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     if resp==True:           
        
        
        lista = Meses.objects.order_by('numero_mes')

                
        if lista:
            result_serializer=MesesSerializers(lista,many=True)

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)
     

@api_view(['POST'])
def GenerarArchivoCsv(request,anno,mes):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
        
        condicion1 = Q(id__exact=id_user)
        datos_usuario=list(Usuarios.objects.filter(condicion1).values())
        
        user=datos_usuario[0]['user_name']
        nombre_user=datos_usuario[0]['nombre_usuario']
        apellido_user=datos_usuario[0]['apellido_usuario']
        correo_user=datos_usuario[0]['correo']

        lista_facturas=registros_facturas(id_user,anno,mes,0)
        
        # lista_egresos_unico = [elemento for elemento in lista_egresos if elemento.get('id') == id]
        
        if lista_facturas:
            
            result_serializer=FacturasSerializer(lista_facturas,many=True)
            ruta=crear_csv_facturas(result_serializer.data,usuario)
            
            nombre_archivo_csv = os.path.basename(ruta)
            Nombre = nombre_user + '; ' + apellido_user
            user_name = user
            html_content = render_to_string('archivo.html', {'Nombre': Nombre, 'user_name': user_name})
            text_content = strip_tags(html_content)
            subject = 'Archivo CSV'
            from_email = 'mytaxesapp@gmail.com'
            to_email = correo_user
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, 'text/html')
            time.sleep(5)
            # with open(ruta, 'rb') as archivo_csv:
            #     email.attach(nombre_archivo_csv, archivo_csv.read(), 'text/csv')  # Adjuntar el archivo CSV
            
            # # Enviar el correo
            # email.send()
            os.remove(ruta) 
            return Response({'mensaje': 'Archivo enviado a ' + correo_user},status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'No tiene movimientos para el periodo seleccionado'},status= status.HTTP_200_OK)
        
    else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)