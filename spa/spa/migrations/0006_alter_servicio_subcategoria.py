# Generated by Django 5.2 on 2025-04-24 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0005_remove_servicio_categoria_servicio_subcategoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spa.subcategoriaservicio'),
        ),
    ]
