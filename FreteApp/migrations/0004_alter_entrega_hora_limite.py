# Generated by Django 4.2.4 on 2023-09-02 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreteApp', '0003_entrega_criado_alter_entrega_hora_limite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='hora_limite',
            field=models.TimeField(blank=True, null=True, verbose_name='Entregar até'),
        ),
    ]