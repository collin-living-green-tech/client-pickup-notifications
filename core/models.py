from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# here we extend the AbstractUser class with our own roles
"""
class User(AbstractUser):

    DEVELOPER = 1
    MANAGEMENT = 2
    OPERATOR = 3
    ROLE_CHOICES = (
        DEVELOPER, 'Developer',
        MANAGEMENT, 'Management',
        OPERATOR, 'Operator'
    )

    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICES, blank=True, null=True)

"""


