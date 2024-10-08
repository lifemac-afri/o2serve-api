# Generated by Django 5.1.1 on 2024-10-02 20:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('table_number', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
