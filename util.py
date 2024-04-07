from datetime import datetime
import time
import googlemaps
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
gmaps = googlemaps.Client(key='AIzaSyCqm0ZSld2E-3SP7Qak_azIQok_fD32hGU')

url = "https://archive-api.open-meteo.com/v1/archive"

def get_coordinates_bulk(addresses):
    geolocator = Nominatim(user_agent="geo_locator")
    coordinates = []
    for address in addresses:
        while True:
            try:
                time.sleep(1)  # Wait for 2 second before retrying
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
    return coordinates
cache = {}
def get_coordinates(address,reference_latitude,reference_longitude,max_retries=2):
    retries = 0
    # Check if the address is already in the cache
    address = address.strip(" ")
    address = address.replace("/","&")
    if address in cache:
        return cache[address]

    while retries < max_retries:
        try:
            time.sleep(1)  # Delay between attempts
            geolocator = Nominatim(user_agent="geo_locator")
            location = geolocator.geocode(address)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                # Store the result in the cache for future use
                cache[address] = (latitude, longitude)
                return latitude, longitude
            else:
                return reference_latitude,reference_longitude
        except Exception as e:
            print(f"Error getting coordinates for address: {address}. Error: {e}")
            print(f"Retry {retries + 1}/{max_retries} in progress...")
            retries += 1

    print(f"Maximum retries ({max_retries}) reached. Coordinates could not be obtained for address: {address}")
    return reference_latitude,reference_latitude


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
        latitude_side = "North"
    elif latitude < reference_latitude:
        latitude_side = "South"
    else:
        latitude_side = "center"

    if longitude > reference_longitude:
        longitude_side = "East"
    elif longitude < reference_longitude:
        longitude_side = "West"
    else:
        longitude_side = "center"

    if latitude_side == "center":
        if longitude_side == "East" : return "E"
        return "W"
    elif longitude_side == "center":
        if latitude_side == "North" : return "N"
        return "S"
    else:
        return f"{latitude_side[0]}{longitude_side[0]}"  # Combine north/south with east/west
def getDateFromTimestamp(timestamp):
    date_obj = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")  # Only date format
    return date_obj.date()

weatherCache = {}

def getWeather(latitude,longitude,timestamp):
    latitude = int(latitude)
    longitude = int(longitude)
    date = getDateFromTimestamp(timestamp)
    key = (latitude,longitude,date)
    if key in weatherCache:
        weatherCodes = weatherCache[key]
        hour = extract_hour_from_timestamp(timestamp)
        return weatherCodes[hour]
    else:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": date,
            "end_date": date,
            "hourly": ["temperature_2m", "precipitation", "weather_code"]
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()

        # Store only weather codes in a list
        weather_codes = hourly_weather_code.tolist()
        print(weather_codes)
        weatherCache[key] = weather_codes

        hour =extract_hour_from_timestamp(timestamp)
        return weather_codes[hour]


def get_coordinates_gmaps(address,reference_latitude,reference_longitude):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
         long = geocode_result[0]['geometry']['location']['lng']
         lat = geocode_result[0]['geometry']['location']['lat']
    else:
        long = reference_longitude
        lat = reference_latitude

    return lat,long

if __name__ == '__main__':
    # date_string = "03/31/2024 0:08"
    # day_of_week = get_day_of_week(date_string.split(" ")[0])
    # print(f"The day of the week for {date_string} is {day_of_week}.")
    # hour = extract_hour_from_timestamp(date_string)
    # print(f"The time of data is: {hour} hours.")
    #
    # # Example usage:
    # address = "3300 HEALTHPLEX PKWY"
    # coordinates = get_coordinates(address)
    # if coordinates:
    #     latitude, longitude = coordinates
    #     print(f"Latitude: {latitude}, Longitude: {longitude}")
    # else:
    #     print("Coordinates not found for the given address.")
    #
    # print(get_town_side(latitude,longitude,35.220833, -97.443611))

    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "start_date": "2024-03-20",
        "end_date": "2024-04-03",
        "hourly": ["temperature_2m", "precipitation", "weather_code"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")



