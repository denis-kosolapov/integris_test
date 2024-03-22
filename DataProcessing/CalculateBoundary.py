from settings import *
import json

j_file = f'{DATA}/data.json'

def calculate_boundary():
    with open(j_file, 'r') as f:
        data = json.load(f)

    latitudes = [point['lat'] for point in data]
    longitudes = [point['lon'] for point in data]

    min_lat = min(latitudes)
    max_lat = max(latitudes)
    min_lon = min(longitudes)
    max_lon = max(longitudes)

    return [
        {'lat': min_lat, 'lon': min_lon},
        {'lat': max_lat, 'lon': min_lon},
        {'lat': max_lat, 'lon': max_lon},
        {'lat': min_lat, 'lon': max_lon}
    ]