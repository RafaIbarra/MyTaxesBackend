from rest_framework import serializers
from MyTaxesBackendApp.models import SolicitudPassword

class SolicitudPasswordSerializers(serializers.ModelSerializer):
    fecha_procesamiento = serializers.DateTimeField(allow_null=True, required=False, default=None, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SolicitudPassword
        fields = '__all__'
    