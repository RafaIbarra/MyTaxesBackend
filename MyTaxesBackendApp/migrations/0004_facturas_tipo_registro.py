# Generated by Django 5.1.2 on 2024-11-18 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyTaxesBackendApp', '0003_alter_empresas_id_alter_facturas_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='tipo_registro',
            field=models.CharField(default='Qr', max_length=200),
        ),
    ]
