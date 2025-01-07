def validaciones_registros(valor,tipo):
    if tipo=='monto':
        if valor is None or valor<1:
            return False
        else:
            return True
        
    if tipo=='fecha_factura':
        
        if valor is None:
            return False
        else:
            fecha = valor.get('fecha_factura')
            if 'fecha_factura' in valor and bool(fecha):
                return True
            else:
                return False
        
        
    