from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from MyTaxesBackendApp.models import Usuarios,SesionesActivas,Meses
from MyTaxesBackendProjects.settings import TIEMPO_SESION_HORAS
from MyTaxesBackendApp.Serializadores.CustomsSerializers import *
from MyTaxesBackendApp.Serializadores.UsuariosSerializer import *
from MyTaxesBackendApp.Serializadores.SesionesActivasSerializers import *

import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status

from rest_framework.response import Response
from ..Seguridad.Validaciones import *
from ..Seguridad.obtener_datos_token import *
import time
import random
import pytz
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from MyTaxesBackendApp.Serializadores.VersionesSerializers import *
from MyTaxesBackendApp.Serializadores.SolicitudPasswordSerializers import *
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        password = request.data.get('password', '')
        version = request.data.get('version', '')
        consulta_version=Versiones.objects.filter(estado__exact=1).values()
        version_sistema=(consulta_version[0]['version']).strip()
        link_descarga=(consulta_version[0]['link_descarga']).strip()

        if 'version' not in request.data:
            
            

            consultausuarios=Usuarios.objects.filter(user_name__exact=user_name).values()
            

            Nombre = str(consultausuarios[0]['nombre_usuario']) + '; ' + str(consultausuarios[0]['apellido_usuario'])
            
            Asunto='Actualizacion de Sistema, se adjunta link de descarga'
            Mensaje=link_descarga

            html_content = render_to_string('archivo.html', 
                                            {'Nombre': Nombre, 
                                            'user_name': user_name,
                                            'Asunto':Asunto,
                                            'Mensaje':Mensaje
                                            })
            
            text_content = strip_tags(html_content)
            subject = 'Actualizacion de la Aplicacion'
            from_email = 'mytaxesapp@gmail.com'
            to_email = str(consultausuarios[0]['correo']) 
            
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            data_errores={
            'mensaje':'Debe actualizar la version, se envio un correo a ' + str(consultausuarios[0]['correo']) ,
            'Version actual':version_sistema,
            'link':link_descarga,
            
            }

            mensaje='Debe actualizar la version, se envio un correo a, ' + str(consultausuarios[0]['correo']) +', con el link de descarga'

            return Response({'error': mensaje}, status=status.HTTP_400_BAD_REQUEST)
        else:
            
            if version_sistema==version:

                registro_sesion=resgistrosesion(user_name)
                
                if registro_sesion:

                    condicion1=Q(user_name__exact=user_name)  
                    tokenusuario=SesionesActivas.objects.filter(condicion1).values()
                    
                    for item in tokenusuario:
                        datotoken=(item['token_session'])
                        condticiontoken=Q(key__exact=datotoken)
                        existetoken=Token.objects.filter(condticiontoken).values()
                        if existetoken:
                            t=Token.objects.get(key=datotoken)
                            t.delete()
                    
                    SesionesActivas.objects.filter(user_name__iexact=user_name).delete()
                    
                user = authenticate(username=user_name,password=password)
                
                if user:
                    user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
                    
                    token,created=Token.objects.get_or_create(user=user)
                
                    consultausuarios=Usuarios.objects.filter(user_name__exact=user).values()
                    
                    fechareg=str(consultausuarios[0]['fecha_registro'])
                    fecha_obj = datetime.fromisoformat(fechareg)
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
                    
                    
                    try:
                
                        datasesion=({
                            'user_name':user_name,
                            'fecha_conexion':datetime.now(),
                            'token_session':token.key,
                            'dispositivo':user_agent
                        })

                        datauser=[{
                            'username':consultausuarios[0]['user_name'].capitalize(),
                            'nombre':consultausuarios[0]['nombre_usuario'],
                            'apellido':consultausuarios[0]['apellido_usuario'],
                            'fecha_registro':fecha_formateada,
                            
                        }

                        ]
                    
                    
                        sesion_serializers=SesionesActivasSerializers(data=datasesion)
                        if sesion_serializers.is_valid():
                            
                            sesion_serializers.save()
                        
                        
                            login_serializer = self.serializer_class(data=request.data)
                            if login_serializer.is_valid():

                                
                                
                                return Response({
                                    'token': login_serializer.validated_data.get('access'),
                                    'refresh': login_serializer.validated_data.get('refresh'),
                                    'sesion':token.key,
                                    'user_name':user_name.capitalize(),
                                    'datauser':datauser,
                                    'message': 'Inicio de Sesion Existoso'
                                }, status=status.HTTP_200_OK)
                            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
                        else :
                            
                            return Response({'error': sesion_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                        

                    except Exception as e:
                        
                        return Response({'message':e.args},status= status.HTTP_406_NOT_ACCEPTABLE)
                        

                return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                data_errores={
                'mensaje':'Debe actualizar la version',
                'link':link_descarga
                }
                return Response({'error':data_errores},status= status.HTTP_406_NOT_ACCEPTABLE)

    
class RegistroUsuario(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            mensajes_error = {}
            nombre = request.data.get('nombre', '')
            apellido = request.data.get('apellido', '')
            nacimiento = request.data.get('nacimiento', '')
            user = request.data.get('user', '')
            correo = request.data.get('correo', '')
            ruc = request.data.get('ruc', '')
            div = request.data.get('div', '')
            nombre_fantasia = request.data.get('fantasia', '')
            password = request.data.get('password', '')
            password=password.replace(" ", "")
            user_reg=formato_user(user)
            condicion1 = Q(username__exact=user_reg)
            existente=User.objects.filter(condicion1).values()

            if not existente:
                
                if not password.strip():  # Verifica si la contraseña está vacía
                    mensajes_error['password']='La contraseña no puede estar vacía' 
                    return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST) 
                
                user_registrar = User.objects.create_user(user_reg, password=password)
                user_registrar.save()
                condicion1 = Q(username__exact=user_reg)
                datosnuevo=list(User.objects.filter(condicion1).values())
                id_nuevo=datosnuevo[0]['id']
                data_user=(
                    {
                        'id':id_nuevo,
                        'nombre_usuario':nombre,
                        'apellido_usuario':apellido,
                        'fecha_nacimiento':nacimiento,
                        'user_name':user_reg,
                        'correo':correo,
                        'ruc':ruc,
                        'div':div,
                        'nombre_fantasia':nombre_fantasia,
                        'ultima_conexion':datetime.now(),
                        'fecha_registro':datetime.now()
                    }
                )
                
                user_serializer=UsuariosSerializer(data=data_user)
                if user_serializer.is_valid():

                    user_serializer.save()
                   
                
                    user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
                    
                    token,created=Token.objects.get_or_create(user=user_registrar)
                
                    datasesion=({
                        'user_name':user_reg,
                        'fecha_conexion':datetime.now(),
                        'token_session':token.key,
                        'dispositivo':user_agent,
                        
                    })

                    sesion_serializers=SesionesActivasSerializers(data=datasesion)
                    if sesion_serializers.is_valid():
                        
                        sesion_serializers.save()
                    
                    
                    datalogin={
                        'username':user_reg,
                        'password':password
                    
                    }
                    
                    login_serializer = self.serializer_class(data=datalogin)
                    if login_serializer.is_valid():
                        consultausuarios=Usuarios.objects.filter(user_name__exact=user_reg).values()
                        fechareg=str(consultausuarios[0]['fecha_registro'])
                        fecha_obj = datetime.fromisoformat(fechareg)
                        fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
                        datauser=[{
                            'username':consultausuarios[0]['user_name'].capitalize(),
                            'nombre':consultausuarios[0]['nombre_usuario'],
                            'apellido':consultausuarios[0]['apellido_usuario'],
                            'fecha_registro':fecha_formateada,
                            
                        }

                        ]

                        Nombre = nombre + '; ' + apellido
                        user_name = user
                        Asunto='Creacion de usuario'
                        Mensaje='Se registro su usuario'

                        html_content = render_to_string('archivo.html', 
                                                        {'Nombre': Nombre, 
                                                        'user_name': user_name,
                                                        'Asunto':Asunto,
                                                        'Mensaje':Mensaje
                                                        })
                        
                        text_content = strip_tags(html_content)
                        subject = 'Inicio Aplicacion'
                        from_email = 'mytaxesapp@gmail.com'
                        to_email = correo
                        
                        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                        email.attach_alternative(html_content, 'text/html')
                        email.send()
                        
                        return Response({
                            'token': login_serializer.validated_data.get('access'),
                            'refresh': login_serializer.validated_data.get('refresh'),
                            'sesion':token.key,
                            'user_name':user_reg.capitalize(),
                            'datauser':datauser,
                            'message': 'Inicio de Sesion Existoso'
                        }, status=status.HTTP_200_OK)
                    
                    
                else :
                    
                   

                    for campo, detalles in user_serializer.errors.items():
                        mensaje = detalles[0]
                        if hasattr(mensaje, 'string'):
                            mensajes_error[campo] = mensaje.string
                        else:
                            mensajes_error[campo] = str(mensaje)

                    user_registrar.delete()
                    return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST)   
        
            else:
                
                mensajes_error['Username']='Ya se creo el usuario ' + user_reg
                return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
                
                return Response({'error':e.args},status= status.HTTP_406_NOT_ACCEPTABLE)
        

@api_view(['POST'])
def comprobarsesionusuario(request):
    
    version=request.data['version']
    
    consulta_version=Versiones.objects.filter(estado__exact=1).values()
    version_sistema=(consulta_version[0]['version']).strip()
    version=version.strip()
    if version_sistema==version:
        token_sesion,usuario,id_user =obtener_datos_token(request)
        resp=validacionpeticion(token_sesion)
        # time.sleep(10)
        if resp==True:
            
            
                consultausuarios=Usuarios.objects.filter(user_name__exact=usuario).values()
                fechareg=str(consultausuarios[0]['fecha_registro'])
                fecha_obj = datetime.fromisoformat(fechareg)
                fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
                datauser=[{
                            'username':consultausuarios[0]['user_name'].capitalize(),
                            'nombre':consultausuarios[0]['nombre_usuario'],
                            'apellido':consultausuarios[0]['apellido_usuario'],
                            'fecha_registro':fecha_formateada,
                            
                        }

                        ] 
                 
                return Response({'datauser':datauser},status= status.HTTP_200_OK)
            
        else:
            return Response(resp,status= status.HTTP_403_FORBIDDEN)
    else:
        
        data_errores={
            'mensaje':'Debe actualizar la version',
            'link':consulta_version[0]['link_descarga'].strip()
        }
        
        return Response({'data':data_errores},status= status.HTTP_400_BAD_REQUEST)
    

class ComprobarVersion(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        version=request.data['version']
        
        consulta_version=Versiones.objects.filter(estado__exact=1).values()
        version_sistema=(consulta_version[0]['version']).strip()
        version=version.strip()
        if version_sistema==version:
           
            return Response({'data':'OK'},status= status.HTTP_200_OK)
                
            
        else:
           
            data_errores={
                'mensaje':'Debe actualizar la version',
                'link':consulta_version[0]['link_descarga'].strip()
            }
            
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
        
class EliminarSesiones(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        
        SesionesActivas.objects.all().delete()
        return Response({"mensaje": "Todas las sesiones han sido eliminadas"}, status=status.HTTP_204_NO_CONTENT)
    
class SolicitudRecuperacionContraseña(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        correo = request.data.get('correo', '')
        user_name=user_name.strip().lower()
        
        consultausuarios=Usuarios.objects.filter(user_name__exact=user_name).values()
        
        if consultausuarios:
            if consultausuarios[0]['correo'].lower()==correo.lower():
                

                Nombre = str(consultausuarios[0]['nombre_usuario']) + '; ' + str(consultausuarios[0]['apellido_usuario'])
                codigo=random.randint(1000, 9999)
                fecha_reg=datetime.now()
                fecha_venc=datetime.now() + timedelta(minutes=60)
                datasave = {
                    "user": consultausuarios[0]['id'],
                    "codigo_recuperacion": codigo,
                    "fecha_creacion": fecha_reg,
                    "fecha_vencimiento": fecha_venc,
                    "codigo_tipo": 2
                }
                solicitud_serializer=SolicitudPasswordSerializers(data=datasave)
                if solicitud_serializer.is_valid():
                    solicitud_serializer.save()

                    Asunto='MY TAXES APP - RECUPERACION CONTRASEÑA'
                    Mensaje='Recuperacion de contraseña para el usuario ' + Nombre
                    Atencion='Para poder realizar la recuperacion de su contraseña debera ingresar el codigo de autenticación.'
                    fecha_validez=fecha_venc.strftime("%d/%m/%Y %H:%M:%S")
                    html_content = render_to_string('pass.html', 
                                                    {'Nombre': Nombre, 
                                                    'user_name': user_name,
                                                    'Asunto':Asunto,
                                                    'Mensaje':Mensaje,
                                                    'Atencion':Atencion,
                                                    'fecha_validez':fecha_validez,
                                                    'codigo':codigo
                                                    })
                    
                    text_content = strip_tags(html_content)
                    subject = 'Recuperacion Contraseña'
                    from_email = 'mytaxesapp@gmail.com'
                    to_email = str(consultausuarios[0]['correo']) 
                    
                    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                    email.attach_alternative(html_content, 'text/html')
                    email.send()
                    #time.sleep(5)

                    

                    mensaje='Se envio un correo a, ' + str(consultausuarios[0]['correo']) +', el codigo de verificacion'

                    # return Response( mensaje, status=status.HTTP_200_OK)
                    return Response({'mensaje': mensaje},status=status.HTTP_200_OK)
                else:
                    
                    return Response({'error':solicitud_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            else:
                
                data_errores={
                'mensaje':'El correo ingresado no coincide con el registrado por el usuario',
                
                }
                return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No existe usuario registrado con el user name ingresado'},status= status.HTTP_400_BAD_REQUEST)
        
class ActualizacionPassword(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        user_name=user_name.strip().lower()
        correo = request.data.get('correo', '')
        passwor1 = request.data.get('password', '')
        passwor2 = request.data.get('password2', '')
        codigo = request.data.get('codigo', '')
        mensajes_error = {}
        user_name=user_name.strip().lower()
        consultausuarios=Usuarios.objects.filter(user_name__exact=user_name).values()
        if consultausuarios:
            id_user=consultausuarios[0]['id']
            result=resultado_codigo(id_user,codigo)
            if not passwor1.strip():  # Verifica si la contraseña está vacía
                        mensajes_error['password']='La contraseña no puede estar vacía' 
                        return Response({'error':mensajes_error},status= status.HTTP_400_BAD_REQUEST) 
            
            if result=='OK':
                if consultausuarios[0]['correo'].lower()==correo.lower() and  passwor1==passwor2:
                    try:
                        usuario=User.objects.get(username=user_name)
                        usuario.set_password(passwor1)
                        usuario.save()

                        condicion1 = Q(codigo_recuperacion__exact=codigo)
                        condicion2= Q(user_id__exact=id_user)
                        datos_solicitud=list(SolicitudPassword.objects.filter(condicion1 & condicion2).values())

                        datasave={
                            "id":  datos_solicitud[0]['id'],
                            "user":  id_user,
                            "codigo_recuperacion": datos_solicitud[0]['codigo_recuperacion'],
                            "fecha_creacion": datos_solicitud[0]['fecha_creacion'],
                            "fecha_vencimiento": datos_solicitud[0]['fecha_vencimiento'],
                            "fecha_procesamiento":datetime.now()
                        }
            
                        condicion=Q(id__exact=datos_solicitud[0]['id'])
                        existente=SolicitudPassword.objects.get(condicion)
                        
                        sol_serializer=SolicitudPasswordSerializers(existente,data=datasave)
                        if sol_serializer.is_valid():
                            sol_serializer.save()
                            return Response({'mensaje': 'Contraseña Actualizada' },status=status.HTTP_200_OK)
                        else:
                            return Response({'error':sol_serializer.errors},status=status.HTTP_400_BAD_REQUEST)    

                    except Exception as e:
                        error=str(e)
                        return Response({'error':error},status=status.HTTP_400_BAD_REQUEST)
                    

                        

                    
                else:
                    mensajeerror=''
                    if consultausuarios[0]['correo'].lower()!=correo.lower():
                        mensajeerror='El correo ingresado no coincide con el registrado por el usuario'
                    
                    if passwor1!=passwor2:
                     
                        if len(mensajeerror) ==0:
                            mensajeerror='Las contraseñas no coinciden'
                        else:
                            mensajeerror=mensajeerror + '; Las contraseñas no coinciden'

                    data_errores={
                    'mensaje':mensajeerror,
                    
                    }
                    return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':result},status= status.HTTP_400_BAD_REQUEST)
            
        return Response({'error':'No existe usuario registrado con el user name ingresado'},status= status.HTTP_400_BAD_REQUEST)
        

class ComprobarCodigoSeguridad(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        user_name = request.data.get('username', '')
        user_name=user_name.strip().lower()
        correo = request.data.get('correo', '')
        
        codigo = request.data.get('codigo', '')
        mensajes_error = {}
        consultausuarios=Usuarios.objects.filter(user_name__exact=user_name).values()
        if consultausuarios:
            id_user=consultausuarios[0]['id']
            result=resultado_codigo(id_user,codigo)
            
            
            if result=='OK':
                
                    if consultausuarios[0]['correo'].lower()==correo.lower():
                        
                        
                        return Response({'mensaje': 'OK' },status=status.HTTP_200_OK)

                    else:
                        mensajeerror=''
                        if consultausuarios[0]['correo'].lower()!=correo.lower():
                            mensajeerror='El correo ingresado no coincide con el registrado por el usuario'
                        
                        data_errores={
                        'mensaje':mensajeerror,
                        
                        }
                        return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'error':result},status= status.HTTP_400_BAD_REQUEST)
        else:
                return Response({'error':'No existe usuario registrado con el user name ingresado'},status= status.HTTP_400_BAD_REQUEST)
        

def formato_user(data):
    
    data = data.replace(" ", "")
    data = data.lower()
    data = re.sub(r'[^a-zA-Z0-9]', '', data)
    return data

def resultado_codigo(id_user,codigo):
    condicion1 = Q(codigo_recuperacion__exact=codigo)
    condicion2= Q(user_id__exact=id_user)
    datos_solicitud=list(SolicitudPassword.objects.filter(condicion1 & condicion2).values())
    
    if len(datos_solicitud) >0:
        fecha_actual = datetime.now()
        
        fecha_vencimiento = datos_solicitud[0]['fecha_vencimiento']
        zona_horaria_correcta = pytz.timezone("America/Asuncion")  # Zona horaria correcta
        fecha_vencimiento = fecha_vencimiento.astimezone(zona_horaria_correcta)

        fecha_actual = fecha_actual.replace(tzinfo=fecha_vencimiento.tzinfo)
        
        fecha_procesamiento=datos_solicitud[0]['fecha_procesamiento']
        errores=''
        if fecha_procesamiento != None:
            errores=errores + 'El codigo ya fue utilizado'

        if fecha_actual> fecha_vencimiento:
            errores=errores + '. El codigo de seguridad ya vencio'
        
        if len(errores) ==0:
            
            return 'OK'
        else:
            return errores
    else:
        return 'El codigo no le pertence al usuario'