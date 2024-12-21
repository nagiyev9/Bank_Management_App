from django.db import models
import uuid

# Account Model
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    profile_url = models.CharField(max_length=255)
    card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True, blank=True)
    transaction_history = models.ManyToManyField('Transaction', blank=True)

# Card Model
class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=23, unique=True)
    card_cvv = models.CharField(max_length=3)
    card_expire_date = models.DateField()
    card_password = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)

# Transaction History Model
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    TRANSACTION_TYPE_CHOICES = [
        ('withdraw', 'Withdraw'),
        ('deposit', 'Deposit'),
        ('money transfer', 'Money Transfer'),
        ('card payment', 'Card Payment')
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    sender_user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='sent_transactions')
    sender_name = models.CharField(max_length=255, null=True, blank=True)
    sender_card = models.CharField(max_length=255, null=True, blank=True)
    reciever_user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='received_transactions')
    reciever_card = models.CharField(max_length=255, null=True, blank=True)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)