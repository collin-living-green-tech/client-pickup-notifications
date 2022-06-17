from django.db import models
from apis.models import Client
# Create your models here.


class Route(models.Model):
    """
    Represents an Living Green Technology
    Electronics recycling Route ,
    with a Client ( to get notifications) ,
    a date when the Route is scheduled to take place
    Latitude, Longitude coordinates
    and an optional field for completed

    """

    Client = models.ForeignKey(Client)
    Date = models.DateField()
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Complete = models.BooleanField(default=False)

