import os
import googlemaps
from googlemaps.exceptions import ApiError, HTTPError
from datetime import datetime


class Route():
    def __init__(self):
        pass

    def query_route(self,start,end):
        gmaps = googlemaps.Client(key='AIzaSyAWuoSydN7jIKsJxjbQz1sfN8ytN30iTwc')

        now = datetime.now()

        try:
            directions_result = gmaps.directions(start, end,
                                                 mode="transit",
                                                 departure_time=now)

            Start_Address,End_Address,Distance,Duration,Step = Route.process_step(self,directions_result)
            
            return Start_Address,End_Address,Distance,Duration,Step

        except (ApiError,HTTPError):
                return None

    def process_step(self, directions):
        Step = []
        legs = directions[0]['legs']
        for leg in legs:
            Start_Address = leg['start_address']
            End_Address = leg['end_address']
            Distance = leg['distance']['text']
            Duration = leg['duration']['text']
            for step in leg['steps']:
                de = {"description": step['html_instructions']}
                Step.append(de)
                if step['travel_mode'] == 'TRANSIT':
                    if step['transit_details']['line']['vehicle']['name'] == 'Bus':
                        bus = {"Bus Information": { "Bus Number": step['transit_details']['line']['short_name'],
                               "Start stop": step['transit_details']['departure_stop']['name'],
                               "Arrive stop": step['transit_details']['arrival_stop']['name'],
                               "Number of stops": step['transit_details']['num_stops']}}
                        Step.append(bus)
                    if step['transit_details']['line']['vehicle']['name'] == 'Subway':
                        sub = {"Subway Information": { "Subway Line": step['transit_details']['line']['name'],
                               "Start stop": step['transit_details']['departure_stop']['name'],
                               "Arrive stop": step['transit_details']['arrival_stop']['name'],
                               "Number of stops": step['transit_details']['num_stops']}}
                        Step.append(sub)
        
        return Start_Address,End_Address,Distance,Duration,Step
        