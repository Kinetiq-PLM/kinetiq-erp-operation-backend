# Generated by Django 5.1.6 on 2025-03-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetRemovalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=255)),
                ('deprecation_report_id', models.CharField(max_length=255)),
                ('reported_date', models.DateField()),
                ('status', models.TextField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending')),
                ('asset_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"operations"."v_asset_removal_view"',
                'ordering': ['external_id'],
                'managed': False,
            },
        ),
    ]
