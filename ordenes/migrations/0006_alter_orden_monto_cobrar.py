# Generated by Django 4.2.1 on 2023-06-24 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0005_productoorden_detalle_alter_productoorden_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='monto_cobrar',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]