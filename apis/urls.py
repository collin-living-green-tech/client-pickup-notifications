from django.urls import path
from .views import ClientCreate,index , RouteCreate, RoutesViewSet, RouteUpdateCreate

app_name='apis'
urlpatterns = [
    path("", index, name='index'),
    path('client/create/',ClientCreate.as_view()),
    path('route/create/', RouteCreate.as_view()),
    path('routes/', RoutesViewSet.as_view({'get':'list'})),
    path('routeupdate/create/', RouteUpdateCreate.as_view()),
]