import datetime

from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.response import  Response

import apis.views
from pickups.models import Route,DailyRoutes
from .models import Client
from .serializers import ClientSerializer, RouteSerializer, RouteUpdateSerializer
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from pickups import RouteStats
from rest_framework.decorators import api_view
from rest_framework.response import Response

import boto3
import os
from pickups.models import DailyRoutes

app = Nominatim(user_agent='tutorial')


from pickups.models import Route, RouteUpdate,Truck


# this is the RouteStats object which
# holds the current state of the current Route

rs = None
# Create your views here.

# a function view to render the
# comingsoon.html page

def index(request):
    return render(request,"apis/comingsoon.html")


class ClientCreate( mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self,request, *args,**kwargs):
        client = Client()
        client.Name = request.POST['Name']
        client.Address = request.POST['Address']
        #client.City = request.POST['City']
        #client.State = request.POST['State']
        #client.Zip = request.POST['Zip']
        client.Email = request.POST['Email']
        client.Phone = request.POST['Phone']
        client.Notify  = True
        client.save()
        client_id = client.id


        return HttpResponse(client_id)


class RouteCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = RouteSerializer

    def post(self, request, *args, **kwargs):
        #route_id  =int(request.POST['id'])
        client_id = request.POST['client_id']
        client = Client.objects.get(pk = client_id)

        #TO DO:


        # implement logic for route update
        # find by hubspot engagement id, if non exists
        # just create new route, otherwise it's an update
        route = Route()
        """
        try:
            route = Route.objects.get(pk = route_id)
        except Exception:
            route = Route()
        """



        #route.id = route_id
        route.Client =client
        route.Date = request.POST['date']
        # To do :
        # add logic to
        # here we resolve the physical
        # address to lat and long coordinates

        locator = Nominatim(user_agent='sojflskdmcpwodas0998887027ew')
        print(locator)
        # build the address string
        address = "{}".format(route.Client.Address)

        location = locator.geocode(address)

        # here we have to verify that
        # the client address was successfully
        # geocoded , otherwise
        # alert the developer Collin Hunt
        if location == None:
            # get the creds
            aws_id = os.environ['aws_id']
            aws_key = os.environ['aws_key']

            #print("info:{}\ninfo:{}\n".format(aws_id,aws_key))
            # setup client with creds
            sns = boto3.client('sns',
                                  region_name='us-west-2',
                                  aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)

            # quickly format the email body with
            # relevant info
            message = """ 
                        **********WARNING************
                        There was an error geocoding 
                        a client pickup address.
                        
                        Time:{}
                        RouteId:{}
                        Address:{}
                        
                        You must input the gps coordinates
                        of the above address for the specified
                        route mainly using the web-app admin
                        page. 
            """
            message = message.format(datetime.datetime.now(),route_id,client.Address)
            sns.publish(TopicArn='arn:aws:sns:us-west-2:573618585260:GeocodingError',
                           Message=message,
                           Subject="****WARNING***** ERROR GEOCODING UPCOMING PICKUP ADDRESS")

            # set route latitude and longitude to 0
            route.DestLat = 0.0
            route.DestLong = 0.0

        else:
            # if it geocode returned an object
            route.DestLat = location.latitude
            route.DestLong = location.longitude

        route.save()
        route_id = route.id


        return HttpResponse(route_id)


class RoutesViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows Routes to be viewed
    """

    def list(self, request):
        queryset = Route.objects.all()
        serializer = RouteSerializer(queryset, many=True)
        return Response( serializer.data)




class RouteUpdateCreate(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = RouteUpdateSerializer

    def post(self, request, *args, **kwargs):
        """

        this endpoint is used by the Android
        app that is inside the pickup vehicle
        that updates its location approx. every
        15 seconds .  Main application logic
        is at this endpoint.   From the gps coordinates
        The state of the 'system' is determined.
        TO DO:
        design the Determin_State capability

        steps for creating a new RouteUpdate object:
            1)  get the current route from the trucks
                table, (should only be 1 record)
                ***** This info should be in memory for
                ***** performance considerations
            2)  use that to set the Route
            3)  set lat , long
            4)  TO DO: Determine state
            5)  save RouteUpdate

        """
        # this is the condition if
        # it is the first update
        # the android app has just started to update its location


        lat = request.POST['lat']
        lng = request.POST['lng']

        res_code = apis.views.rs.get_state(lat,lng)
        if res_code == -1:
            """
                here we send the code to terminate the
                android updates , b/c there are no
                more routes for the day 
            """


        resp_str = "Lat:{},Long:{},Resp:{}".format(request.POST['lat'],request.POST['lng'],res_code)
        return HttpResponse(resp_str)


def print_time():
    """
    just a test function to
    test django schedules
    Returns:

    """
    print(datetime.datetime.now())



@api_view()
def start_day(request):
    """
    This endpoint is used by the
    android app when it is first
    started at the beginning of the
    day.  This will initialize
    a new RouteStats object
    if their are Routes in the DailyRotues
    table.  Otherwise just tells the android
    app to go ahead and terminate
    """

    # first check the number of DailyRoutes
    no_daily_routes = len(DailyRoutes.objects.all())
    if no_daily_routes != 0:
        daily_pickups = DailyRoutes.objects.all()
        apis.views.rs = RouteStats.RouteStats(daily_pickups)

    return Response({"Response": no_daily_routes})