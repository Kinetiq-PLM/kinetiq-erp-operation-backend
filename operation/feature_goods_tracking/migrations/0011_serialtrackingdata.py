# Generated by Django 5.1.6 on 2025-04-14 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_goods_tracking', '0010_departmentdata_employeedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='SerialTrackingData',
            fields=[
                ('serial_id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('serial_no', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"operations"."serial_tracking"',
                'ordering': ['serial_no'],
                'managed': False,
            },
        ),
    ]
