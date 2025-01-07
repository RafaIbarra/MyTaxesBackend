from MyTaxesBackendApp.models import SesionesActivas,Usuarios
def obtener_datos_token(request):
    token=request.data['SESION']
    id_user=0
    datotoken=SesionesActivas.objects.filter(token_session__exact=token).values()
    if datotoken:
        usuario=datotoken[0]['user_name']
        u=Usuarios.objects.filter(user_name=usuario).values()
        id_user=u[0]['id']
    else: 
        usuario=''
    return token,usuario,id_user