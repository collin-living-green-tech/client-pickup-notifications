import datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import DailyRoutes, Route
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import DailyRoutesForm

from django.forms import modelformset_factory

# Create your views here.




def confirm_dailyroutesorder(request):
    """
    Uses a formset to
    set the DailyRoutes order
    Args:
        request:

    Returns:

    """

    DailyRoutesFormSet = modelformset_factory(DailyRoutes, fields=('Order', 'Route'))
    form = DailyRoutesFormSet(queryset=DailyRoutes.objects.all())
    if request.method == 'POST':
            form = DailyRoutesFormSet(request.POST)
            form.save()



    return render(request,'pickups/dailyroutes.html', {'form': form})

def dailyroutes_list(request):
    """
    lists the routes contained
    in the dailyroutes table
    allows the operator to reorder
    the routes in dailyroutes
    to suite their needs,
    and then confirm
    """
    dailyroutes = DailyRoutes.objects.all()

    return render(request,'pickups/dailyroutes.html',{'routes':dailyroutes})


@require_POST
def save_new_ordering(request):
    """
    this is the view to submit the
    new order of dailyroutes

    """
    form = DailyRoutesForm(request.POST)

    if form.is_valid():
        ordered_ids = form.cleaned_data["ordering"].split(',')

        with transaction.atomic():
            current_order = 1
            for lookup_id in ordered_ids:
                lookup_id = lookup_id.replace('"','')
                group = DailyRoutes.objects.get(id=lookup_id)
                group.Order = current_order
                group.save()
                current_order += 1

        return redirect('apis:index')


def test_cron():
    """
    just a method for testing
    django_crontab.  Appends the time
    to a file
    """
    with open('scheduled_op.txt','wa') as fp:
        fp.write(str(datetime.datetime.now()))



def NewDailyRoutes():
    """
    clears the previous DailyRoutes table
    and repopulates it with
    routes scheduled for current date, with no specific ordering
    TO DO:
    implement operator routeorder confirmation
    notification
    Returns:

    """

    DailyRoutes.objects.all().delete()

    # filter routes by todays date
    todays_routes = Route.objects.get(Date=datetime.date.today())

    idx = 1
    for route in todays_routes:
        dr = DailyRoutes(idx,route)
        dr.save()
        idx+= 1

    # TO DO: initialize RouteStats object









