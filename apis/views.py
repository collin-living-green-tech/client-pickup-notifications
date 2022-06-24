from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.response import  Response
from .models import Client
from .serializers import ClientSerializer, RouteSerializer, RouteUpdateSerializer
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from pickups.models import DailyRoutes

app = Nominatim(user_agent='tutorial')

from pickups.models import Route, RouteUpdate,Truck
# Create your views here.

# a function view to render the
# comingsoon.html page

def index(request):
    return render(request,"apis/comingsoon.html")


class ClientCreate( mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self,request, *args,**kwargs):
        return self.create(request, *args, **kwargs)


class RouteCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = RouteSerializer

    def post(self, request, *args, **kwargs):
        client_id = request.POST['client_id']
        client = Client.objects.get(pk = client_id)
        route = Route()
        route.Client =client
        route.Date = request.POST['date']
        # To do :
        # add logic to
        # here we resolve the physical
        # address to lat and long coordinates
        locator = Nominatim(user_agent='client pickup notifications')
        # build the address string
        address = "{},{},{},{}".format(route.Client.Address, route.Client.City, route.Client.State, route.Client.Zip)
        location = locator.geocode(address)
        route.DestLat = location.latitude
        route.DestLong = location.longitude
        route.save()
        route_id = route.id

        # if the route is for today,
        # we add it to the DailyRoutes table
        # and leave the order blank
        order = len(DailyRoutes.objects.all())+1
        dailyRoute = DailyRoutes(Order=order,Route=route)
        dailyRoute.save()
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
        resp_str = "Lat:{},Long:{}".format(request.POST['lat'],request.POST['long'])
        return HttpResponse(resp_str)



