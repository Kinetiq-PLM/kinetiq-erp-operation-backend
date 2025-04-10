# Generated by Django 5.1.6 on 2025-03-30 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_internal_transfer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalTransferReworkOrderData',
            fields=[
                ('external_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('product_id', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('rework_notes', models.CharField(max_length=255)),
                ('selling_price', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
    ]
