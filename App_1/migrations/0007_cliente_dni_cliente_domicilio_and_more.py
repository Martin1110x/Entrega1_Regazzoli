# Generated by Django 4.1 on 2022-10-11 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0006_alter_avatar_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='DNI',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='domicilio',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_de_nacimiento',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='provincia',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
