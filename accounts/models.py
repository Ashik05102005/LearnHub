from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)

    address = models.TextField(
        blank=True , null = True
    )
    date_of_birth = models.DateField(
        blank=True , null=True
    )
