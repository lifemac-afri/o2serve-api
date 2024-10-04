# Generated by Django 5.1.1 on 2024-10-04 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
