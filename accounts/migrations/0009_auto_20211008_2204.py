# Generated by Django 3.2.8 on 2021-10-08 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20211008_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='date_created',
        ),
        migrations.DeleteModel(
            name='CompletedOrder',
        ),
    ]