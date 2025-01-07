from rest_framework import serializers

class ResumenPeriodoSerializers(serializers.Serializer):
   
    AnnoFactura =serializers.IntegerField()
    MesFactura =serializers.CharField(max_length=200,allow_blank=True)
    NombreMesFactura =serializers.CharField(max_length=200,allow_blank=True)    
    Periodo  =serializers.CharField(max_length=200,allow_blank=True)
    TotalFacturas=serializers.IntegerField()  
    TotalIva10=serializers.IntegerField()  
    TotalIva5=serializers.IntegerField()
    TotalLiquidacionIva=serializers.IntegerField()
    CantidadRegistros=serializers.IntegerField()
    

    def validate(self,data):
        return data