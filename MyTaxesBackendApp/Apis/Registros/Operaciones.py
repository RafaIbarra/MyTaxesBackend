from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from django.db.models import Q


from datetime import datetime
import json
import ast

from ..Seguridad.obtener_datos_token import *
from ..Seguridad.Validaciones import *
from .validacion_datos import *
from MyTaxesBackendApp.Serializadores.EmpresasSerializers import *
from MyTaxesBackendApp.Serializadores.FacturasSerializers import *
from MyTaxesBackendApp.Serializadores.FacturasDetalleSerializers import *
from MyTaxesBackendApp.models import *
import time
@api_view(['POST'])
def registrofactura(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        data_list = []
        data_errores=''
        campos_requeridos = ["concepto","cantidad", "total"]
        
        detalle_factura=json.loads(request.data['detallefactura'])
        
        id_factura=int(request.data['codfactura'])
        ruc_empresa=request.data['rucempresa']
        nombre_empresa=request.data['nombreempresa']
        tipo_registro=request.data['tiporegistro']
        
        
        
        controlcampos=True
        for item in detalle_factura:
            for campo in campos_requeridos:
                if campo not in item:
                    controlcampos=False
                    
        if controlcampos!=True:
            suma_montos=0
            mensaje='Falta de detalle facturas'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        if controlcampos:
             suma_montos = sum(item['total'] for item in detalle_factura)

        if suma_montos<1:
            mensaje='El monto no puede ser menor a 1'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        if len(request.data['numero_factura']) < 10:
            mensaje='La numeracion de facturas debe componerse de al menos 10 numeros'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        if len(request.data['rucempresa']) < 1:
            mensaje='Ingrese el ruc de la empresa'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje
        
        if validaciones_registros(request.data,'fecha_factura'):
            fecha_obj = datetime.strptime(request.data['fecha_factura'], '%Y-%m-%d')
            anno=fecha_obj.year
            mes=fecha_obj.month
        else: 
            mensaje='Seleccione una fecha'
            data_errores = data_errores + mensaje if len(data_errores) == 0 else data_errores + '; ' + mensaje

        condicion_empresa1 = Q(ruc_empresa__exact=ruc_empresa)
        empresa_existente=Empresas.objects.filter(condicion_empresa1)
        if empresa_existente:
            pass
        else:
            
            empresa_save={
                "id":0,
                "nombre_empresa":nombre_empresa,
                "ruc_empresa":ruc_empresa,
                "fecha_registro": datetime.now()
            }
            
            empresa_serializer=EmpresasSerializer(data=empresa_save)
            if empresa_serializer.is_valid():
                empresa_serializer.save()
            else:
                
                return Response({'error':empresa_serializer.errors},status= status.HTTP_400_BAD_REQUEST)

        
        empresa_registro=Empresas.objects.filter(condicion_empresa1).values()
        id_empresa=empresa_registro[0]['id']
        
        
        
        if len(data_errores)==0:
            datasave={
                "id":request.data['codfactura'],
                "user": id_user,
                "empresa":  id_empresa,
                "numero_factura":  request.data['numero_factura'],
                "fecha_factura": request.data['fecha_factura'],
                "total_factura": request.data['total_factura'],
                "iva10": request.data['iva10'],
                "iva5": request.data['iva5'],
                "liquidacion_iva": request.data['liquidacion_iva'],
                "cdc": request.data['cdc'],
                "tipo_registro":tipo_registro,
                "fecha_registro": datetime.now()
            
            }
            data_list.append(datasave)
            if id_factura>0:
                
                condicion1 = Q(id__exact=id_factura)
                dato_existente=Facturas.objects.filter(condicion1)
                if dato_existente:
                    
                    existente=Facturas.objects.get(condicion1)
                    
                    factura_serializer=FacturasSerializer(existente,data=datasave)

                else:
                    return Response({'message':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
                

            else:
                if tipo_registro.lower()!='manual':
                    condicion_cdc = Q(cdc__exact=request.data['cdc'])
                    cdc_existente=Facturas.objects.filter(condicion_cdc)
                    # print(cdc_existente)
                    if cdc_existente:
                        return Response({'error':'La factura con el cdc ya fue registrado'},status= status.HTTP_400_BAD_REQUEST)

                factura_serializer=FacturasSerializer(data=datasave)
            
            

            if factura_serializer.is_valid():
                
                factura_instance =factura_serializer.save()
                
                id_factura_gen=factura_instance.id
                
                if id_factura == 0:
                    id_factura_gen=factura_instance.id
                    for item in detalle_factura:
                        item['factura'] = id_factura_gen
                        item['fecha_registro']= datetime.now()
                    
                    FacturasDetalle.objects.filter(factura_id=id_factura_gen).delete()
                    serializer = FacturasDetalleSerializer(data=detalle_factura, many=True)
                    if serializer.is_valid():
                        serializer.save()
                        # data=datos_resumen(id_user,anno,mes)
                        return Response({'mensaje':'Registro Factura Almacenado'},status= status.HTTP_200_OK)
                    else:
                        
                        t=Facturas.objects.get(id=id_factura_gen)
                        t.delete()
                        return Response({'mensaje':serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
                else:
                    
                    registros_existentes = FacturasDetalle.objects.filter(factura_id=id_factura)
                    registros_existentes_dict = [
                        {"concepto": registro.concepto, "cantidad": registro.cantidad, "total": registro.total}
                        for registro in registros_existentes
                    ]
  
                    
                    
                    registros_coincidentes = [registro for registro in detalle_factura if registro in registros_existentes_dict]
                    registros_no_enviados = [registro for registro in registros_existentes_dict if registro not in detalle_factura]
                    registros_nuevos = [registro for registro in detalle_factura if registro not in registros_existentes_dict]
                    # print('registros_coincidentes',registros_coincidentes)
                    # print('registros_no_enviados',registros_no_enviados)
                    


                    for item in detalle_factura:
                        item['factura'] = id_factura_gen
                        item['fecha_registro']= datetime.now()

                    if len(registros_no_enviados) >0 or len(registros_nuevos)>0:
                        
                        FacturasDetalle.objects.filter(factura_id=id_factura).delete()
                        
                        serializer = FacturasDetalleSerializer(data=detalle_factura, many=True)
                        if serializer.is_valid():
                            serializer.save()
                            # data=datos_resumen(id_user,anno,mes)
                            return Response({'mensaje':'Registro Factura Almacenado'},status= status.HTTP_200_OK)
                        else:
                            
                            return Response({'error':serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje':'Registro Factura Almacenado'},status= status.HTTP_200_OK)

                    
                    # return Response([],status= status.HTTP_200_OK)

                
            else:
                
                # return Response({'message':factura_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                return Response({'error':'error en registro de facturas'},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':data_errores},status= status.HTTP_400_BAD_REQUEST)

        # return Response([],status= status.HTTP_200_OK)

    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def eliminarfactura(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    if resp==True:
         
        facturasdel=request.data['facturaseliminar']

        if type(facturasdel)==str:
            facturasdel=ast.literal_eval(facturasdel)

        if len(facturasdel)>0:
            for item in facturasdel:
                condicion1 = Q(id__exact=item)
                lista=Facturas.objects.filter(condicion1).values()
                if lista:
        
                    factura = Facturas.objects.get(pk=item)
                    factura.delete()
                    return Response({'message':'Facturas Eliminadas'},status= status.HTTP_200_OK)
                else:
                    return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)

        else:
            return Response({'message':'No hay registros que eliminar'},status= status.HTTP_200_OK)
    else:
         return Response(resp,status= status.HTTP_403_FORBIDDEN)
    



