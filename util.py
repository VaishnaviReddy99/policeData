from datetime import datetime
import time

from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim


def get_coordinates_bulk(addresses):
    geolocator = Nominatim(user_agent="geo_locator")
    coordinates = []
    for address in addresses:
        while True:
            try:
                location = geolocator.geocode(address)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    coordinates.append((latitude, longitude))
                else:
                    coordinates.append(None)
                break  # Break out of the retry loop if geocoding succeeds
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(e)
                print(f"Geocoding request failed for address: {address}. Retrying after 1 second...")
                time.sleep(1)  # Wait for 1 second before retrying
            print(coordinates)
    return coordinates
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None



def get_day_of_week(date_string):
    # Assuming date_string is in the format "YYYY-MM-DD"
    date_obj = datetime.strptime(date_string, "%m/%d/%Y %H:%M")
    day_of_week = date_obj.weekday()  # Monday is 0 and Sunday is 6
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day_of_week]

def extract_hour_from_timestamp(timestamp):
    # Assuming timestamp is in the format "YYYY-MM-DD H:MM"
    date_obj = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
    hour = date_obj.hour
    return hour
def get_town_side(latitude, longitude, reference_latitude, reference_longitude):
    if latitude > reference_latitude:
        latitude_side = "north"
    elif latitude < reference_latitude:
        latitude_side = "south"
    else:
        latitude_side = "center"

    if longitude > reference_longitude:
        longitude_side = "east"
    elif longitude < reference_longitude:
        longitude_side = "west"
    else:
        longitude_side = "center"

    return latitude_side, longitude_side
if __name__ == '__main__':
    date_string = "2022-03-31 0:08"
    day_of_week = get_day_of_week(date_string.split(" ")[0])
    print(f"The day of the week for {date_string} is {day_of_week}.")
    hour = extract_hour_from_timestamp(date_string)
    print(f"The time of data is: {hour} hours.")

    # Example usage:
    address = "3300 HEALTHPLEX PKWY"
    coordinates = get_coordinates(address)
    if coordinates:
        latitude, longitude = coordinates
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Coordinates not found for the given address.")

    print(get_town_side(latitude,longitude,35.220833, -97.443611))

