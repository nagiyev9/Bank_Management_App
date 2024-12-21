from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

MALE = 'M'
FEMALE = 'F'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.CharField(
        max_length=1,
        choices=[
            (MALE, 'Male'),
            (FEMALE, 'Female')
        ]
    )
    email = models.EmailField(
        unique=True
    )
    number = models.CharField(max_length=25)
    birthday_date = models.DateField()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
