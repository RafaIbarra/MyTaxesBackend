# Generated by Django 5.1.2 on 2024-11-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyTaxesBackendApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='cdc',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
