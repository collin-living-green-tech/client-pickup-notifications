import datetime
import math
from collections import deque
from enum import Enum, IntEnum

from django.utils import timezone

import pickups.models
from pickups.models import MovingAverage


lgt_bounds = ( # latitude range
    [47.3245, 47.325,
    # longitude range
    -122.252,-122.2498 ])

# origin when starting at lgt auburn
LGT_ORIGIN = ([47.324890, -122.251273])

MILES_DEGS = 53.00

class RouteStats:
    """
    Used to hold stats on the
    current route , as well as maintain
    the list of dailyroutes in order
    as a queue

    """

    def __init__(self, daily_routes):
        self.pickups = deque()

        # create the routes queue in route order
        for route in sorted(list(daily_routes),key=lambda x: x.Order, reverse=True):
            self.pickups.append(route)

        self.no_pickups = len(self.pickups)
        self.pickups_complete = 0
        # set initial distance to first daily pickup
        self.distance = self.get_distance(LGT_ORIGIN[0], LGT_ORIGIN[1])
        self.prevState = State.AT_ORIGIN

        # TO DO:  get running avg
        self.mvgAvg = MovingAverage.objects.get(pk=1).mpm

        # TO DO: implement
        self.eta_mins = self.get_eta()


        self.threshold = 5.0

        # equivalent to 300 ft approx.
        self.arrived_thrhld = .056818

        self.last_update = datetime.datetime.now()





    def get_distance(self,lat2,lng2):
        """
        calculates the distance in
        miles from current location
        to current route destination
        Note: constant latitude degrees is 53 miles
        Args:
            lat2:
            lng2:

        Returns:

        """
        lat_diff = abs(self.pickups[0].Route.DestLat - float(lat2))
        long_diff = abs(self.pickups[0].Route.DestLong - float(lng2))
        hyp_diff = math.sqrt( lat_diff**2 + long_diff**2)

        return hyp_diff * MILES_DEGS

    def get_eta(self):
        """
        returns approximate eta to
        current route destination
        based on moving average
        and current distance to destination
        Returns:

        """
        return self.distance / self.mvgAvg


    def get_state(self, lat, lng):
        """
        main application logic
        determines the current state of
        the system
        Args:
            lat: gps latitude in degrees
            lng: gps longitude in degrees

        Returns: an integer indicating the number
        of routes not complete or 0 if their are no more
        sets self.prevState to State enum value

        """
        # just for the first update of the
        # day


        curr_dist = self.get_distance(lat,lng)
        last_state= self.prevState

        # check if coordinates are within
        # range of still being at living green technology or previous route origin
        lat = float(lat)
        lng = float(lng)


        if lat > lgt_bounds[0] and lat < lgt_bounds[1] and lng > lgt_bounds[3] and lng < lgt_bounds[2]:
            self.prevState = State.AT_ORIGIN

        # check for enroute
        elif curr_dist < self.distance:
            self.prevState = State.ENROUTE
            # check for arriving shortly , basically
            # if distance is less than global threshold
            if curr_dist < self.threshold:
                self.prevState = State.ARRIVING_SHORTLY

            # arrived state
            if curr_dist <= self.arrived_thrhld:
                self.prevState = State.ARRIVED


        # check for stationary
        elif curr_dist == self.distance:

            self.prevState = State.STATIONARY
            # TO DO :
            # check if stationary after having
            # arrived ,
            # either switch to next route in pickups , or turn off
            # updates
            self.pickups_complete+=1
            if last_state == State.ARRIVED:
                # check if there are more routes to perform
                if self.pickups_complete != self.no_pickups:

                    coord_diff = .000394/2
                    # switch origin , deque current route
                    prevRoute = self.pickups.popleft()
                    # set origin to prevRoute coordinates range
                    lgt_bounds[0] = prevRoute.Latitude + coord_diff
                    lgt_bounds[1] = prevRoute.Latitude - coord_diff
                    lgt_bounds[2] = prevRoute.Longitude - coord_diff
                    lgt_bounds[3] = prevRoute.Longitude + coord_diff



        # check for indeterminate state
        elif curr_dist > self.distance:
            self.prevState = State.INDETERMINATE



        prevState_int = int(self.prevState)

        # TO DO: update stats ( mvgAvg, eta)  if state is ENROUTE, STATIONARY , OR INDETERMINATE, ARRIVING_SHORTLY
        if prevState_int > 2:
            self.update_avg(curr_dist, datetime.datetime.now())
            self.distance = curr_dist

        # TO DO: create RouteUpdate object if state is anything other than AT_LGT
        if prevState_int > 1:
            """
            update current members for saving
            """

            self.route_update(lat,lng)

        return self.no_pickups - self.pickups_complete




    def route_update(self,lat,lng):
        """
        saves the current RouteStats data
        into RouteUpdate
        Returns:

        """
        update = pickups.models.RouteUpdate()
        update.Route = self.pickups[0].Route
        update.State = self.prevState
        update.Lat =  lat
        update.Long = lng
        tz = timezone.get_current_timezone()
        timzone_datetime = timezone.make_aware(datetime.datetime.now(), tz, True)

        update.Stamp = timzone_datetime
        update.save()


    def update_avg(self, dist, ts):
        """
        used to update moving average and recalculate eta based on
        new average
        """
        self.mvgAvg  = (self.mvgAvg + dist ) / ((ts - self.last_update).total_seconds() / 60)
        self.eta = self.distance / self.mvgAvg






class State(IntEnum):
    AT_ORIGIN = 1
    ARRIVED = 2
    ENROUTE = 3
    INDETERMINATE = 4
    STATIONARY = 5
    ARRIVING_SHORTLY = 6







