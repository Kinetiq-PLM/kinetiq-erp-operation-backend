# Generated by Django 5.1.6 on 2025-04-15 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feature_get_reference_data', '0004_customerdata'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customerdata',
            table='"sales"."customers"',
        ),
    ]
