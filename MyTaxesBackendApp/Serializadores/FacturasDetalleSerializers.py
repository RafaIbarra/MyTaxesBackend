from rest_framework import serializers
from MyTaxesBackendApp.models import FacturasDetalle

class FacturasDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacturasDetalle
        fields= '__all__'
        
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')