from rest_framework import serializers
from pickups.models import  Route, RouteUpdate, Truck
from .models import Client



class ClientSerializer( serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ( 'Name','Address','City','State','Zip','Email','Phone','ContactPreference','Notify')


class RouteSerializer( serializers.ModelSerializer):
    Client = ClientSerializer()

    class Meta:
        model = Route
        fields = ('Client', 'Date')

