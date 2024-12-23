# Generated by Django 5.1.4 on 2024-12-18 18:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('card_number', models.CharField(max_length=19, unique=True)),
                ('card_cvv', models.CharField(max_length=3)),
                ('card_expire_date', models.DateField()),
                ('card_password', models.CharField(max_length=4)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('balance_after_transaction', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('receiver_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('profile_url', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.card')),
                ('transaction_history', models.ManyToManyField(blank=True, to='account.transaction')),
            ],
        ),
    ]
