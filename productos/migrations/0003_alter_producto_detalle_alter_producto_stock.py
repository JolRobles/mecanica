# Generated by Django 4.2.1 on 2023-06-02 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_producto_pvp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='detalle',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
