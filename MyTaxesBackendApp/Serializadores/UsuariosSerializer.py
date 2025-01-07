from rest_framework import serializers
from MyTaxesBackendApp.models import Usuarios

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuarios
        fields= '__all__'
        
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    ultima_conexion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')