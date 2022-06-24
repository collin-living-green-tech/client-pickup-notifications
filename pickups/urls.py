

from django.urls import path
from . import views
from .views import dailyroutes_list,save_new_ordering

app_name='pickups'

urlpatterns = [
    path('dailyroutes/', dailyroutes_list),
    path('save-item-ordering',save_new_ordering, name='save-item-ordering')
]