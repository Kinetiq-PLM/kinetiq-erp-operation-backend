# Generated by Django 5.1.6 on 2025-04-12 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_internal_transfer', '0003_sendtodistributiondata_updatedeliveryrequestdata_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionOrderData',
            fields=[
                ('production_order_detail_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('actual_quantity', models.PositiveIntegerField()),
                ('rework_required', models.BooleanField(default=False)),
                ('rework_notes', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"production"."production_orders_details"',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalModuleProductOrderData',
            fields=[
                ('external_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('rework_quantity', models.PositiveIntegerField()),
                ('reason_rework', models.CharField(max_length=255)),
                ('production_order_detail_id', models.ForeignKey(blank=True, db_column='production_order_detail_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature_internal_transfer.productionorderdata')),
            ],
        ),
        migrations.DeleteModel(
            name='InternalTransferReworkOrderData',
        ),
    ]
