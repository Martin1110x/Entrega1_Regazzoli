# Generated by Django 4.1 on 2022-10-11 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0008_remove_empleado_apellido_remove_empleado_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferencia_bancaria',
            name='id_transferencia',
        ),
    ]
