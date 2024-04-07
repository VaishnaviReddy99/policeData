import pytest
import util
def test_getCoordinates():
    address = "1600 Pennsylvania Ave NW, Washington, DC"
    reference_latitude = 38.89
    reference_longitude = -77.0

    latitude, longitude = util.get_coordinates(address, reference_latitude, reference_longitude)

    # Assert that the returned coordinates are not the reference values
    assert latitude != reference_latitude
    assert longitude != reference_longitude


def test_DayAndHour():
    date_string = "04/07/2024 15:30"

    day_of_week = util.get_day_of_week(date_string)
    hour = util.extract_hour_from_timestamp(date_string)

    # Assert expected day and hour values
    assert day_of_week == "Sunday"
    assert hour == 15

def test_get_town_side():
  # Test North-East
  latitude = 35.3
  longitude = -98.6
  reference_latitude = 35.2
  reference_longitude = -97.4
  assert util.get_town_side(latitude, longitude, reference_latitude, reference_longitude) == "NW"
