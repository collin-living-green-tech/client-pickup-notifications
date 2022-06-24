from django.contrib import admin
from .models import Route, DailyRoutes
# Register your models here.


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = [ 'Client',  'Date']


@admin.register(DailyRoutes)
class DailyRoutesAdmin(admin.ModelAdmin):
    list_display = [ 'Order','Route']