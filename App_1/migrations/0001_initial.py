# Generated by Django 4.1 on 2022-09-05 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('DNI', models.IntegerField()),
                ('nivel_del_cliente', models.CharField(max_length=40)),
                ('dinero_en_la_cuenta', models.IntegerField()),
                ('tarjeta_de_credito_vencida', models.BooleanField()),
                ('fecha_de_vencimiento_tarjeta', models.DateField()),
                ('numero_de_tarjeta', models.IntegerField()),
                ('codigo_de_seguridad_tarjeta', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('DNI', models.IntegerField()),
                ('posicion_laboral', models.CharField(max_length=40)),
                ('fecha_de_ingreso_a_la_empresa', models.DateField()),
                ('sueldo_en_pesos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transferencias_bancarias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_transferencia', models.IntegerField()),
                ('monto_en_pesos', models.IntegerField()),
                ('fecha_de_transferencia', models.DateField()),
                ('nombre_del_remitente', models.CharField(max_length=40)),
                ('apellido_del_remitente', models.CharField(max_length=40)),
                ('dni_del_remitente', models.IntegerField()),
                ('nombre_del_destinatario', models.CharField(max_length=40)),
                ('apellido_del_destinatario', models.CharField(max_length=40)),
                ('dni_del_destinatario', models.IntegerField()),
                ('destinatario_cliente_del_banco', models.BooleanField()),
            ],
        ),
    ]
