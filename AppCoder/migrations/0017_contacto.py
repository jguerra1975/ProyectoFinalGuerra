# Generated by Django 4.2.4 on 2023-10-08 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0016_alter_comentarioarticulos_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_consulta', models.ImageField(choices=[[0, 'Consulta'], [0, 'Reclamo'], [0, 'Sugerencia'], [0, 'Felicitaciones']], upload_to='')),
                ('mensaje', models.TextField()),
                ('avisos', models.BooleanField()),
            ],
        ),
    ]
