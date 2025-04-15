# Generated by Django 5.1.6 on 2025-04-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_get_reference_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetData',
            fields=[
                ('asset_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('asset_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"admin"."assets"',
                'ordering': ['asset_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MaterialData',
            fields=[
                ('material_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('material_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"admin"."raw_materials"',
                'ordering': ['material_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('product_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('produt_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"admin"."products"',
                'ordering': ['product_id'],
                'managed': False,
            },
        ),
    ]
