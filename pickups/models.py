from django.db import models
from apis.models import Client
import datetime
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

    Client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Date = models.DateField()
    DestLat = models.FloatField()
    DestLong = models.FloatField()
    Complete = models.BooleanField(default=False)


class State(models.Model):
    """
    A table for holding the various states
    during a Route
    at LGT
    ENROUTE
    INDETERMINATE
    STATIONARY
    ARRIVING_SHORTLY
    ARRIVED
    """
    Name=models.CharField(max_length=20)

class RouteUpdate(models.Model):
    """
    Represents a node on the path from
    the start of a Route to the Routes destination
    holds the time , and position of LGT pickup truck
    as well as the State, i.e. enroute , indeterminate, stationary, close , arrived

    """
    Route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    Lat = models.FloatField()
    Long = models.FloatField()
    Stamp = models.DateTimeField(default=datetime.datetime.now())
    State = models.ForeignKey(State, on_delete=models.DO_NOTHING)




class Truck(models.Model):
    CurrentRoute = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    #DailyRoutes = models.ManyToManyField(Route)



