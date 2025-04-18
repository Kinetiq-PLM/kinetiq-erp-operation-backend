# Generated by Django 5.1.6 on 2025-04-05 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseQuotationData',
            fields=[
                ('quotation_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('status', models.TextField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending')),
                ('document_no', models.PositiveIntegerField()),
                ('document_date', models.TextField()),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('freight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': '"purchase"."purchase_quotation"',
                'ordering': ['quotation_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequestData',
            fields=[
                ('request_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('material_id', models.CharField(max_length=255)),
                ('asset_id', models.CharField(max_length=255)),
                ('purchase_quantity', models.PositiveIntegerField()),
            ],
            options={
                'db_table': '"purchase"."purchase_requests"',
                'ordering': ['request_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuotationContentsData',
            fields=[
                ('quotation_content_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': '"purchase"."quotation_contents"',
                'ordering': ['quotation_content_id'],
                'managed': False,
            },
        ),
    ]
