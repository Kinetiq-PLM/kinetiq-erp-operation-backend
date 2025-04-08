# Generated by Django 5.1.6 on 2025-03-29 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='updateDeliveryApprovalData',
            fields=[
                ('approval_request_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('request_date', models.DateField()),
                ('approval_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')])),
                ('approval_date', models.DateField()),
                ('approved_by', models.CharField(max_length=100)),
            ],
            options={
                'db_table': '"distribution"."logistics_approval_request"',
                'ordering': ['approval_request_id'],
                'managed': False,
            },
        ),
    ]
