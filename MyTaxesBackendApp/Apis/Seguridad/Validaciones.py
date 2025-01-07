from MyTaxesBackendApp.models import	SesionesActivas,Usuarios
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

def resgistrosesion(nombreusuario):
    result=False
    condicion1=Q(user_name__iexact=nombreusuario)
    dato=SesionesActivas.objects.filter(condicion1)
    if dato.exists():
        result=True
    return result


def validaciones( tokensesion):
    mensajevalidacion=''
    sesionvalida=True
    datos_token=Token.objects.filter(key__exact=tokensesion).values()
    if datos_token:
        sesion_token=SesionesActivas.objects.filter(token_session__exact=tokensesion).values()

        if sesion_token:
             user_id_token=datos_token[0]['user_id']
             user_token_sesion=sesion_token[0]['user_name']
             datos_user_sesion_token=Usuarios.objects.filter(user_name__exact=user_token_sesion).values()
             user_id_token_sesion=datos_user_sesion_token[0]['id']

             if user_id_token_sesion!= user_id_token:
                mensajevalidacion='El usuario del Token no coincide con el token en la sesion'
                sesionvalida=False   

        else:
            mensajevalidacion='El token no le pertenece a ninguna sesion'
            sesionvalida=False
    else:
        mensajevalidacion='El token no existe'
        sesionvalida=False

        
    return sesionvalida,mensajevalidacion


def validacionpeticion(tokensesion):
   
    
    token_sesion=tokensesion
    controlsesion,mensajesesion=validaciones(token_sesion)
   
    if controlsesion:
        
        return True
    else:
        return {
                'mensajesesion':mensajesesion,
                'controltoken':controlsesion,
                
            }


