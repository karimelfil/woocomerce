# Generated by Django 5.0.6 on 2024-06-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_alter_woocomerceuser_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]