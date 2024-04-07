import pytest
import csv
import assignment2 as assign

def test_parse_csv():
  data = [["col1", "col2"], ["data1", "data2"]]
  with open("test.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

  parsed_data = assign.parse_csv("test.csv")
  assert parsed_data == data

  # Cleanup
  import os
  os.remove("test.csv")


def test_incident_augmented():
  day_of_week = "Monday"
  time_of_day = 12
  weather = "Sunny"
  location_rank = 1
  side_of_town = "North"
  incident_rank = 2
  nature = "Medical"
  ems_stat = True

  incident = assign.IncidentAugmented(day_of_week, time_of_day, weather, location_rank,
                               side_of_town, incident_rank, nature, ems_stat)

  assert incident.day_of_week == day_of_week
  assert incident.time_of_day == time_of_day

  # Assert to_list method
  expected_list = [day_of_week, time_of_day, weather, location_rank, side_of_town, incident_rank, nature, ems_stat]
  assert incident.to_list() == expected_list

