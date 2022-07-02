from rest_framework import serializers
from pickups.models import  Route, RouteUpdate, Truck
from .models import Client



class ClientSerializer( serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ( 'Name','Address','City','Email','Phone')


class RouteSerializer( serializers.ModelSerializer):
    Client = ClientSerializer()

    class Meta:
        model = Route
        fields = ('id','Client', 'Date','DestLat','DestLong')

class RouteUpdateSerializer( serializers.ModelSerializer):
    Route = RouteSerializer()

    class meta:
        model = RouteUpdate
        fields = '__all__'
