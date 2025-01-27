from django.db import models

# Create your models here.

class Usuarios(models.Model):
    
    id= models.IntegerField(primary_key=True, serialize=False)
    nombre_usuario=models.CharField(max_length=200,blank=False)
    apellido_usuario=models.CharField(max_length=200,blank=False)
    fecha_nacimiento=models.DateField("Fecha Nacimiento")
    user_name=models.CharField(max_length=100,blank=False,unique=True)
    correo=models.EmailField(blank=True)
    ruc=models.IntegerField()
    div=models.IntegerField()
    nombre_fantasia=models.CharField(max_length=200,blank=True)
    ultima_conexion=models.DateTimeField("fecha ultma conexion")
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Usuarios"


class Empresas(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    nombre_empresa=models.CharField(max_length=200,blank=False)
    ruc_empresa=models.CharField(max_length=200,blank=False,unique=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Empresas"

    


class Facturas(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    empresa=models.ForeignKey(Empresas, on_delete=models.CASCADE, default=1)
    numero_factura=models.CharField(max_length=200,blank=False)
    fecha_factura=models.DateTimeField("fecha factura")
    total_factura=models.IntegerField()
    iva10=models.IntegerField()
    iva5=models.IntegerField()
    liquidacion_iva=models.IntegerField()
    cdc=models.CharField(max_length=200,blank=True)
    tipo_registro=models.CharField(max_length=200,blank=False,default='Qr')
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Facturas"

    def retorno_empresa_id(self):
        return self.empresa_id


class FacturasDetalle(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    # factura=models.ForeignKey(Facturas, on_delete=models.CASCADE, default=1)
    factura = models.ForeignKey(Facturas, related_name='detalles', on_delete=models.CASCADE)
    concepto=models.CharField(max_length=200,blank=False)
    cantidad=models.CharField(max_length=10,blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="FacturasDetalle"



class SesionesActivas(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user_name=models.CharField(max_length=100,blank=False)
    fecha_conexion=models.DateTimeField("fecha ultma conexion")
    token_session=models.CharField(max_length=100,blank=True)
    dispositivo=models.CharField(max_length=200,blank=True)
    
    class Meta:
        db_table="SesionesActivas"

    def __str__(self):
        return (f"{self.user_name.capitalize()} , {self.user_name.capitalize()}")
    

class Meses(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    numero_mes=models.IntegerField( default=1)
    nombre_mes=models.CharField(max_length=100,blank=False)
    fecha_registro=models.DateTimeField("fecha_registro")
    
    class Meta:
        db_table="Meses"

    def __str__(self):
        return (f"{self.nombre_mes.capitalize()} , {self.nombre_mes.capitalize()}")
    

class SolicitudPassword(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    codigo_recuperacion=models.IntegerField()
    fecha_creacion=models.DateTimeField("fecha creacion",blank=False)
    fecha_vencimiento=models.DateTimeField("fecha vencimiento",blank=False)
    fecha_procesamiento=models.DateTimeField("fecha vencimiento",blank=True,null=True)

    class Meta:
        db_table="SolicitudPassword"
