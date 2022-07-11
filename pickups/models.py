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

    def __str__(self):
        return self.Client.Name  + str(self.Date)



class RouteUpdate(models.Model):
    """
    Represents a node on the path from
    the start of a Route to the Routes destination
    holds the time , and position of LGT pickup truck
    as well as the State, i.e. enroute , indeterminate, stationary, close , arrived

    """


    Route = models.ForeignKey(Route, on_delete=models.CASCADE)
    Lat = models.FloatField()
    Long = models.FloatField()
    Stamp = models.DateTimeField(default=datetime.datetime.now())

    # the five choices , enroute , at_LGT, indeterminate, stationary, arriving_shortly, arrived
    STATE_CHOICES = ( (1,'at lgt'),
                      (2,'enroute'),
                      (3,'indeterminate'),
                      (4,'stationary'),
                      (5,'arriving shortly'),
                      (6,'arrived'))
    State = models.IntegerField(choices=STATE_CHOICES)

class Truck(models.Model):
    CurrentRoute = models.ForeignKey(Route, on_delete=models.CASCADE)
    #DailyRoutes = models.ManyToManyField(Route)



class DailyRoutes(models.Model):
    """
    Represents the list of
    pickups that are scheduled
    for the current date ONLY
    ENTIRE TABLE IS DROPPED at the beginning of the
    day , and repopulated with TODAYS routes only
    only fields are , Order , and route foreign key
    """

    Order = models.IntegerField(null=True)
    Route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return  self.Route.__str__()


class MovingAverage(models.Model):
        """
        holds the current moving avg in
        miles per minute
        """
        mpm = models.FloatField()

