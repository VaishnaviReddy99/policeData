# cis6930sp24 -- Assignment2

Name: Sree Vaishnavi Madireddy

UFID: 87626790

# Assignment Description 
This assignment focuses on augmenting police incident data (extracted from PDFs in Assignment 0) with contextual details like weather and location. Additionally, a comprehensive data sheet will be created to document the enriched dataset, following established best practices.

# How to install
pipenv install

## How to run
    pipenv run python assignment2.py --urls <file_name>

It can be run as follows:

![](https://github.com/VaishnaviReddy99/cis6930sp24-assignment2/blob/main/output.gif)



## Functions
#### assignment0\main.py \
This file is responsible to fetch data from the Given URLS and parse the pdfs to get Incident data

#### assignment2.py \
This is the main file responsible for the task

    create_excel_sheet(filename, data): t creates a new Excel sheet using the openpyxl library and writes the provided data to the sheet. In this case AugmentedData.xlsx is created.
    
    parse_csv(filename): This function parses a CSV file specified by the filename (string) argument using the csv library. It reads the data row by row and returns a list of lists, where each inner list represents a row from the CSV file.
    
    calculate_ranks(incidents): This function takes a list of IncidentAugmented objects as input (incidents).
    It calculates two types of ranks:
        Location Rank: It analyzes the frequency of incident locations in the data. Locations appearing more frequently receive a higher rank.
        Incident Rank: It analyzes the frequency of incident natures in the data. Incidents of a particular nature occurring more frequently receive a higher rank.
    
    main(filename): This function drives the script's execution, processing incident data from a CSV file, enriching it with external information, calculating ranks, and ultimately generating an Excel sheet with the augmented results.

#### util.py \
    This script provides helper functions for various tasks related to incident data processing.

    get_coordinates(address, reference_latitude, reference_longitude, max_retries=2): Retrieves latitude and longitude for a single address, using caching and retries. Returns reference coordinates if geocoding fails.

    get_day_of_week(date_string): Extracts the day of the week (e.g., "Monday") from a date string in the format "MM/DD/YYYY HH:MM".
    
    extract_hour_from_timestamp(timestamp): Extracts the hour as an integer value (0-23) from a timestamp string in the format "MM/DD/YYYY HH:MM".

    get_town_side(latitude, longitude, reference_latitude, reference_longitude):  Determines the "side of town" (e.g., "NW", "SE") based on latitude and longitude coordinates relative to reference coordinates.
    
    getDateFromTimestamp(timestamp): Extracts only the date (without time) as a datetime.date object from a timestamp string in the format "MM/DD/YYYY HH:MM".

    getWeather(latitude, longitude, timestamp): Retrieves weather codes for a given latitude, longitude, and timestamp using the Open-Meteo API, with caching for efficiency.

    get_coordinates_gmaps(address, reference_latitude, reference_longitude): Retrieves latitude and longitude for an address using the Google Maps Geocoding API. Returns reference coordinates if geocoding fails.

#### test_assignment2.py \
This file conducts unit tests for functions within assignment2.py. The pytest framework is employed for testing purposes.

    test_parse_csv(): This test validates the capabilities of the parse_csv function to accurately extract data from a CSV file.
    
    test_incident_augmented(): This test ensures the correct functionality of the IncidentAugmented class, including its initialization and ability to create a list representation of incident data.
    
#### test_util.py \
This file contains unit tests for functionalities used in assignment2.py. It utilizes the pytest framework for testing.

    test_getCoordinates(): This test verifies that the get_coordinates function from util.py retrieves coordinates different from the provided reference point.
    
    test_DayAndHour(): This test ensures that the get_day_of_week and extract_hour_from_timestamp functions from util.py correctly extract the day of the week and hour from a given date-time string.

    test_get_town_side(): This test checks the functionality of the get_town_side function util.py , in determining the side of town based on coordinates and a reference point.
 
    
## Datasheet Development
The datasheet is created as DATASHEET.md 
This file contains all the information related to the given dataset

## Assumptions
a. The URLs are always provided in a CSV file. It assumes the CSV file contains URLs or some identifier for fetching additional details about each incident.

b. The util.py script retrieves reference coordinates (reference_latitude and reference_longitude) for situations where geocoding fails.

c. Date/Time, Incident Number, Incident ORI cannot be null/empty

d. The script assumes specific formats for timestamps (likely "MM/DD/YYYY HH:MM") used in the data.

e. Both scripts might require additional setup for external API access (e.g., API keys).   

f. To optimize calls to the weather API, we're exploring the idea of using only the integer portion (whole number part) of the latitude and longitude coordinates when fetching weather data for incidents

## Bugs
If the incident's nature is present but the location is not, or vice versa, the script would encounter a failure, preventing it from parsing the entire data file.

The code assumes that weather patterns are similar for locations with the same integer part of their latitude and longitude. While this can be a good optimization for reducing weather API calls, it might lead to inaccurate weather data for incidents in close proximity but with slightly different coordinates



