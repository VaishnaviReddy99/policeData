import csv
from openpyxl import Workbook

import assignment0.main
import util
from assignment0 import main


incident_rank = {}


class IncidentAugmented:
    def __init__(self, day_of_week, time_of_day, weather, location_rank, side_of_town, incident_rank, nature, ems_stat):
        self.day_of_week = day_of_week
        self.time_of_day = time_of_day
        self.weather = weather
        self.location_rank = location_rank
        self.side_of_town = side_of_town
        self.incident_rank = incident_rank
        self.nature = nature
        self.ems_stat = ems_stat

    def to_list(self):
        return [self.day_of_week, self.time_of_day, self.weather, self.location_rank,
                self.side_of_town, self.incident_rank, self.nature, self.ems_stat]


def create_excel_sheet(filename, data):
    wb = Workbook()
    ws = wb.active

    for row in data:
        print(row)
        ws.append(row)

    wb.save(filename)
    print(f"Excel sheet '{filename}' created successfully!")




def parse_csv(filename):
    data = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def calculate_ranks(incidents ):
    locationFreq = {}
    natureFreq = {}
    for inc in incidents:
        if inc.nature in natureFreq:
            natureFreq[inc.nature] += 1
        else:
            natureFreq[inc.nature] = 1
        if inc.incident_location in locationFreq:
            natureFreq[inc.incident_location] += 1
        else:
            natureFreq[inc.incident_location] = 1

    sorted_frequency = sorted(natureFreq.items(), key=lambda x: x[1], reverse=True)
    rank = 1
    ranks = {}
    prev_count = None
    for element, count in sorted_frequency:
        if count != prev_count:
            rank = len(ranks) + 1
        ranks[element] = rank
        prev_count = count

    sorted_frequency = sorted(natureFreq.items(), key=lambda x: x[1], reverse=True)
    rank = 1
    locationRanks = {}
    prev_count = None
    for element, count in sorted_frequency:
        if count != prev_count:
            rank = len(ranks) + 1
        locationRanks[element] = rank
        prev_count = count


    return ranks,locationRanks




def main():
    filename = "files.csv"
    parsed_data = parse_csv(filename)
    augmented_data = list()
    augmented_data.append(["Day Of the Week", "Time of Day", "Weather", "Location Rank","Side of Town", "Incident Rank","Nature","EMSSTAT"])
    count = 0
    for pd in parsed_data:
        for data in pd:
            if data:
                results = assignment0.main.parseAndFetchResults(data)
                incidentRanks,location_ranks = calculate_ranks(results)
                addresses = list()
                for result in results:
                    day = util.get_day_of_week(result.incident_time)
                    timeOfDay = util.extract_hour_from_timestamp(result.incident_time)
                    weather_of_inc = "***placeholder***"
                    location_rank = location_ranks[result.incident_location]
                    sideOfTown = "SE"
                    incident_rank = incidentRanks[result.nature]
                    nature = result.nature
                    emstatt = False
                    if result.incident_ori == "EMSSTAT":
                        emstatt = True
                    if result.incident_location:
                        addresses.append(result.incident_location)
                    ia = IncidentAugmented(day,timeOfDay,weather_of_inc,location_rank,sideOfTown,incident_rank,nature,emstatt)
                    augmented_data.append(IncidentAugmented.to_list(ia))
                    count = count + 1
    filename = "DATASHEET.xlsx"
    create_excel_sheet(filename, augmented_data)


if __name__ == "__main__":
    main()
