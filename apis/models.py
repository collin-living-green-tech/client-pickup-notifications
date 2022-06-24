from django.db import models

# Create your models here.

class Client(models.Model):
    """
    Represents a living green technology Client
    a company whose contact info is stored in
    this model , so an entity can be associated with
    a pickup

    """
    Name = models.CharField(max_length=200)
    Address = models.CharField( max_length = 200)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=2)
    Zip = models.IntegerField()
    Email = models.EmailField(null=True)
    Phone = models.IntegerField(null=True)
    ContactPreference = models.CharField(max_length=5)
    Notify = models.BooleanField(default=True)

    def __str__(self):
        return self.Name




