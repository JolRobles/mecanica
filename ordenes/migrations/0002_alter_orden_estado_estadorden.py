# Generated by Django 4.2.1 on 2023-05-26 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_empresa'),
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='estado',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='ordenes.estado'),
        ),
        migrations.CreateModel(
            name='EstadOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateTimeField(auto_now=True)),
                ('estado', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='ordenes.estado')),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ordenes.orden')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuario')),
            ],
            options={
                'verbose_name': 'estadOrden',
                'verbose_name_plural': 'estadOrdenes',
            },
        ),
    ]
