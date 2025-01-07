from rest_framework import serializers
from MyTaxesBackendApp.models import Empresas

class EmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Empresas
        fields= '__all__'
        
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    