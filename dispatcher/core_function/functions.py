from django.conf import settings
import requests
import math


def get_info(start_location, end_location, waypoints):
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    route_legs = []

    waypoint_str = 'optimize:true|' + '|'.join(waypoints) if waypoints else None

    params = {
        'origin': start_location,
        'destination': end_location,
        'key': api_key,
        'mode': 'DRIVING',
        'waypoints': waypoint_str,

    }

    # Send request to Google Maps Directions API
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        # Extract travel time and route legs from the response
        total_time = 0
        total_sec = 8 * 60 * 60
        for leg in data['routes'][0]['legs']:
            route_legs.append({
                'start_address': leg['start_address'],
                'end_address': leg['end_address'],
                'distance': leg['distance']['text'],
                'distance_value': leg['distance']['value'],
                'duration': leg['duration']['text'],
                'time_travel': math.ceil((total_time + int(leg['duration']['value']) / 60)),
                'time': add_seconds_to_time(total_sec + (leg['duration']['value'])),
                'total_sec': total_sec + (leg['duration']['value']),
            })
            total_time = math.ceil((total_time + leg['duration']['value']) / 60)
            total_sec = total_sec + int(leg['duration']['value'])
    return route_legs


def add_seconds_to_time(seconds):
    # Calculate new hours, minutes, and seconds
    new_hours = (seconds // 3600) % 24  # Wrap around at 24 hours
    new_minutes = math.ceil((seconds % 3600) / 60)

    return f"{new_hours:02}:{new_minutes:02}"
