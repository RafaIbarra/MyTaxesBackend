from rest_framework.response import Response
from rest_framework import status  
from rest_framework_simplejwt.views import TokenObtainPairView
from MyTaxesBackendApp.Serializadores.CustomsSerializers import *
from MyTaxesBackendApp.Serializadores.VersionesSerializers import *
from datetime import datetime
class RegistroVersion(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        version = request.data.get('version', '').strip()
        link_descarga = request.data.get('link', '').strip()
        descripcion = request.data.get('descripcion', '').strip()
        save={
                "id":0,
                "version":version,
                "link_descarga":link_descarga,
                "descripcion": descripcion,
                "estado": 1,
                "fecha_creacion": datetime.now()
            }
        version_serializer=VersionesSerializers(data=save)
        if version_serializer.is_valid():
            Versiones.objects.all().update(estado=2)
            version_serializer.save()
            return Response({'mensaje':'Version Registrada'},status= status.HTTP_200_OK)

        else:
                
             return Response({'error':version_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
