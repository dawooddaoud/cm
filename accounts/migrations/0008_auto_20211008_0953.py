# Generated by Django 3.2.8 on 2021-10-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_product_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.CreateModel(
            name='CompletedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ManyToManyField(to='accounts.Customer')),
                ('product', models.ManyToManyField(to='accounts.Product')),
            ],
        ),
    ]
