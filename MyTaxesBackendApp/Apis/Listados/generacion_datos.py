from django.db.models import Q
import pandas as pd
from datetime import datetime
from MyTaxesBackendApp.models import *
from MyTaxesBackendApp.Serializadores.FacturasSerializers import *
import csv
import os

def registros_facturas(user,anno,mes,id):
    condicion1 = Q(user_id__exact=user)
    condicion_id= Q(id__exact=id)

    if anno >0:
        condicion2 = Q(fecha_factura__year=anno)
        
        if mes>0:
            condicion3 = Q(fecha_factura__month=mes)
            if id>0:
                lista=Facturas.objects.filter(condicion1 & condicion2 & condicion3 & condicion_id)
            else:
                lista=Facturas.objects.filter(condicion1 & condicion2 & condicion3)
        else:
            if id>0:
                lista=Facturas.objects.filter(condicion1 & condicion2 & condicion_id)
            else:
                lista=Facturas.objects.filter(condicion1 & condicion2)
    else:
        if id>0:
            lista=Facturas.objects.filter(condicion1 & condicion_id)
        else:
            lista=Facturas.objects.filter(condicion1 )
    
    lista_datos=lista


    if lista_datos:
        return lista_datos
            
    else:
        []


def resumen_periodo(user,anno):
    data_facturas=registros_facturas(user,anno,0,0)
    if data_facturas:
        data_factura_serializer=FacturasSerializer(data_facturas,many=True)
        df_data_facturas=pd.DataFrame(data_factura_serializer.data)
        df_data_facturas['Periodo']=df_data_facturas['NombreMesFactura'] + '-' + df_data_facturas['AnnoFactura'].astype(str)
        df_data_facturas=df_data_facturas.reset_index()
        

        df_data_factura_agrupado = df_data_facturas.groupby(['AnnoFactura', 'MesFactura','NombreMesFactura','Periodo']).agg(
            TotalFacturas=('total_factura', 'sum'),
            TotalIva10=('iva10', 'sum'),
            TotalIva5=('iva5', 'sum'),
            TotalLiquidacionIva=('liquidacion_iva', 'sum'),
            CantidadRegistros=('total_factura', 'count')
            ).reset_index()
        
        df_data_factura_agrupado = df_data_factura_agrupado.sort_values(by=['AnnoFactura', 'MesFactura'], ascending=[True, True])
        df_data_factura_agrupado = df_data_factura_agrupado.reset_index()
        

        data_list = df_data_factura_agrupado.to_dict(orient='records')

        return data_list
    


def crear_csv_facturas(datos,usuario):
    ruta_actual = os.getcwd()  # Obtiene la ruta actual del proyecto
    nombrearchivo=usuario +'.csv'
    ruta_archivo = os.path.join(ruta_actual, nombrearchivo)
    with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, delimiter=';')
        
        # Escribir la cabecera
        escritor.writerow(['Fecha Factura', 'Numero Factura', 'Total Factura', 'IVA 10%', 'IVA 5%', 'Liquidacion IVA', 'RUC Empresa', 'Nombre Empresa'])
        
        # Escribir los datos
        for factura in datos:
            escritor.writerow([
                factura['fecha_factura'],
                factura['numero_factura'],
                factura['total_factura'],
                factura['iva10'],
                factura['iva5'],
                factura['liquidacion_iva'],
                factura['RucEmpresa'],
                factura['NombreEmpresa']
            ])
    return ruta_archivo
    