from rest_framework import serializers
from MyTaxesBackendApp.models import Facturas,Empresas,FacturasDetalle,Meses

class FacturasSerializer(serializers.ModelSerializer):
    NombreEmpresa=serializers.SerializerMethodField()
    RucEmpresa=serializers.SerializerMethodField()
    DetalleFactura=serializers.SerializerMethodField()
    MesFactura=serializers.SerializerMethodField()
    NombreMesFactura=serializers.SerializerMethodField()
    AnnoFactura=serializers.SerializerMethodField()
    class Meta:
        model=Facturas
        
        fields= [
                "id" ,
                "fecha_registro",
                "numero_factura",
                "fecha_factura",
                "MesFactura",
                "NombreMesFactura",
                "AnnoFactura",
                "total_factura",
                "iva10",
                "iva5",
                "liquidacion_iva",
                "cdc",
                "tipo_registro",
                "user",
                "empresa",
                "NombreEmpresa",
                "RucEmpresa",
                "DetalleFactura"
                ]
        
    def get_DetalleFactura(self, obj):
        
        try:
            # condicion2 = Q(egresos_id=cod_gasto)
            result=[]
            detalles_obj = FacturasDetalle.objects.filter(factura_id=obj.id).values()
            for elemento in detalles_obj:
                
                
                valores={
                    "id":elemento['id'],
                    "Concepto":elemento['concepto'],
                    "Cantidad":elemento['cantidad'],
                    "Total":elemento['total'],
                    
                }
                result.append(valores)
            return result
        except FacturasDetalle.DoesNotExist:
            return None
    def get_NombreEmpresa(self, obj):
        
        cod_empresa = obj.retorno_empresa_id()
        try:
            empresa_obj = Empresas.objects.get(id=cod_empresa)
            return empresa_obj.nombre_empresa
        except Empresas.DoesNotExist:
            return None
        
    def get_RucEmpresa(self, obj):
        
        cod_empresa = obj.retorno_empresa_id()
        try:
            empresa_obj = Empresas.objects.get(id=cod_empresa)
            return empresa_obj.ruc_empresa
        except Empresas.DoesNotExist:
            return None
        
    def get_MesFactura(self, obj):
        return obj.fecha_factura.month
    
    def get_NombreMesFactura(self, obj):
        numeromes= obj.fecha_factura.month
        try:
            mes_obj = Meses.objects.get(numero_mes=numeromes)
            return mes_obj.nombre_mes
        except Meses.DoesNotExist:
            return None
    
    def get_AnnoFactura(self, obj):
        return obj.fecha_factura.year
        

    # fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    fecha_registro = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')
    fecha_factura = serializers.DateTimeField(format='%d/%m/%Y')