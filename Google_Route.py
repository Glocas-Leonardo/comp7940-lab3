import os
import googlemaps
from datetime import datetime


class Route():
    def __init__(self):
        pass

    def query_route(self,start,end):
        gmaps = googlemaps.Client(key='AIzaSyAWuoSydN7jIKsJxjbQz1sfN8ytN30iTwc')

        now = datetime.now()

        directions_result = gmaps.directions(start, end,
                                             mode="transit",
                                             departure_time=now)
        return directions_result
        