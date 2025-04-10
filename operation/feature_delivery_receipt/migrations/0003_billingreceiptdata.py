# Generated by Django 5.1.6 on 2025-03-27 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_delivery_receipt', '0002_deliveryreceiptdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingReceiptData',
            fields=[
                ('external_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('billing_receipt_id', models.CharField(max_length=255)),
                ('delivery_receipt_id', models.CharField(max_length=255)),
                ('delivery_date', models.DateField()),
                ('total_receipt', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': '"operations"."v_delivery_billing_receipt_view"',
                'ordering': ['external_id'],
                'managed': False,
            },
        ),
    ]
