# Generated by Django 5.1.6 on 2025-04-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_goods_tracking', '0007_alter_productdocuitemdata_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCostData',
            fields=[
                ('bom_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('product_id', models.CharField(max_length=255)),
                ('cost_of_production', models.DecimalField(decimal_places=2, max_digits=10)),
                ('miscellaneous_costs', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': '"operations"."v_product_details_view"',
                'ordering': ['bom_id'],
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='productdocuitemdata',
            table='"operations"."product_document_items"',
        ),
    ]
