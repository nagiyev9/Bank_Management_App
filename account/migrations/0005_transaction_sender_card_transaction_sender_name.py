# Generated by Django 5.1.4 on 2024-12-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_card_card_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sender_card',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
