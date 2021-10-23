import requests
import json
import directions_cache
import polyline
from subprocess import check_output


def get_directions_for_zones(fromZone, toZone, API_KEY):

    fromZoneGoogleCoordinates = f'{str(fromZone[1])},{str(fromZone[0])}'
    toZoneGoogleCoordinates = f'{str(toZone[1])},{str(toZone[0])}'

    if not directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates):
        directions = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={fromZoneGoogleCoordinates}&destination={toZoneGoogleCoordinates}&key={API_KEY}')
        directions_cache.put(fromZoneGoogleCoordinates, toZoneGoogleCoordinates, directions.json())
        
        print('Received data from Google maps')

    summary = directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates)['routes'][0]['summary']
    pointsAlongLine = directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates)['routes'][0]['overview_polyline']['points']
    print(json.dumps(summary, indent=4))

    pointsAlongLine = list(map(list, polyline.decode(pointsAlongLine)))

    with open(f'./data/pointsAlongLine.json', "w") as jsonFile:
        json.dump({'pointsAlongLine': pointsAlongLine}, jsonFile)

    print(check_output(f"node polyline/dead_battery_points.js ", shell=True))


# ZONE_COUNT = 5
API_KEY = input('Enter API key\n')


#Read centroids_in_zones.json
json_file = "centroids_in_zones.json"
Centroids_zones = dict()

with open(json_file) as _Centroid_zones:
    Centroids_zones = json.load(_Centroid_zones)

ZoneId_ = []
Coordinate_ = []

for point in Centroids_zones['features']:
    zoneId = point['properties']['Id']
    ZoneId_.append(zoneId)

for coordinate in Centroids_zones['features']:
    coordinate_ = coordinate['geometry']['coordinates']
    Coordinate_.append(coordinate_)
# print(ZoneId_)
# print(Coordinate_)
# Required_5zones = dict(zip(ZoneId_,Coordinate_))
# print(Required_5zones)


# for fromZone i 1 to ZONE_COUNT
#     for toZone j 1 to ZONE_COUNT 
#           if i != j

for i in range(len(ZoneId_)):
    for j in range(len(ZoneId_)):
        if i != j:
            get_directions_for_zones(Coordinate_[i], Coordinate_[j], API_KEY)



