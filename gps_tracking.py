from typing import List
import gmplot

class Coordinates:
    def __init__(self, message_type: str, time_stamp: float, latitude:float, 
    lat_denotation: str, longitude: float, long_denotation: str):
        self.message_type = message_type
        self.time_stamp = time_stamp
        self.latitude = latitude
        self.lat_denotation = lat_denotation
        self.longitude = longitude
        self.long_denotation = long_denotation

coordinates_list = List[Coordinates]

def parse_latitude(lattitude) -> float:
    degrees = lattitude[0:2]
    converted_minutes = str(float(lattitude[2::]) / 60)
    return float(degrees + converted_minutes[1::])

def parse_longitude(longitude)-> float:
    degrees = longitude[0:3]
    converted_minutes = str(float(longitude[3::]) / 60)
    return float(degrees + converted_minutes[1::])

def parese_time_stamp(time_stamp: str) -> str:
    return f'{time_stamp[0:2]}:{time_stamp[2:4]}:{time_stamp[4:6]}'

def parse_log_file(file_name: str) -> coordinates_list:
    coordinates_list = []
    with open(f'template/{file_name}') as infile:
        for line in infile:
            data = line.split(',')
            if data[0] == '$GPGGA':
                coordinates_list.append(Coordinates(data[0],parese_time_stamp(data[1]), parse_latitude(data[2]), data[3], parse_longitude(data[4]), data[5]))
            else:
                print(data[0] + ' message was not parsed. Reason: IRELEVANT/INVALID')
    print('***Data has been parsed. Ivalid or irelevant data were skipped***')
    return coordinates_list


def draw_map(coordinates_list: List[Coordinates]) -> None:
    apikey = ''
    gmap = gmplot.GoogleMapPlotter(coordinates_list[0].latitude, coordinates_list[0].longitude,17, apikey=apikey)
    gmap.marker(coordinates_list[0].latitude, coordinates_list[0].longitude, color='blue') # Strting point
    for coordinate in coordinates_list:
        gmap.marker(coordinate.latitude, coordinate.longitude, color='green')
    gmap.marker(coordinates_list[-1].latitude, coordinates_list[-1].longitude, color='red') # End Point
    gmap.draw('map.html')
    print('***The map.html has been generated***')
    print('***To acces the map you can open map.html in your browser***')
    print('***Route STARTS AT BLUE marker and ENDS AT RED marker***')

# TO DO
coordinates_list = parse_log_file('log.txt')
draw_map(coordinates_list) # map.html has been drawn. You can open it in your browser to track Karliks friend movemet
