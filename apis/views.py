from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.response import  Response
from .models import Client
from .serializers import ClientSerializer, RouteSerializer
from django.http import HttpResponse

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
        route.DestLat = 100.0
        route.DestLong = 100.0
        route.save()

        return HttpResponse("Route Created ?")


class RoutesViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows Routes to be viewed
    """

    def list(self, request):
        queryset = Route.objects.all()
        serializer = RouteSerializer(queryset, many=True)
        return Response( serializer.data)







