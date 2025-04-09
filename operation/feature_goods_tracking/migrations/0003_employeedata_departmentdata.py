# Generated by Django 5.1.6 on 2025-04-03 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_goods_tracking', '0002_vendordata'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeData',
            fields=[
                ('employee_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '"human_resources"."employees"',
                'ordering': ['employee_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentData',
            fields=[
                ('dept_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=255)),
            ],
        ),
    ]
