import io
import re
import requests
import sqlite3
import os
import argparse
from pypdf import PdfReader


class Incident:
    def __init__(self, incident_time, incident_number, incident_location, nature, incident_ori):
        self.incident_time = incident_time
        self.incident_number = incident_number
        self.incident_location = incident_location
        self.nature = nature
        self.incident_ori = incident_ori

    @classmethod
    def print_members(cls, incident):
        for key, value in incident.__dict__.items():
            print(f"{key}: {value}")

create_query = ''' CREATE TABLE if not exists incidents (
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT ); '''
drop_query = 'DROP TABLE IF EXISTS incidents'
count_incidents_query = 'select count(*) from incidents'
sql_insert = ''' INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
    VALUES (?, ?, ?, ?, ?) '''
nature_type_query = '''SELECT nature,count(*) as natureCount from incidents group by nature order by natureCount desc, CASE WHEN nature = '' THEN 1 ELSE 0 END, nature '''
db_location = "resources/normanpd.db"


def parseUrl(sampleUrl):
    sqliteConn = connectAndTestDB()

    results = parseAndFetchResults(sampleUrl)

    insertResultSet(results,sqliteConn)
    result = natureTypeState(sqliteConn)
    for row in result:
        print(row[0], "|", row[1], sep="")

    sqliteConn.close()





def parseAndFetchResults(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching URL response aborting process")
        return
    reader = PdfReader(io.BytesIO(response.content))
    resultSet = list()
    pages = reader.pages
    for page in pages:
        rset = parseEachPage(page)
        resultSet.extend(rset)
    return resultSet



def parseEachPage(page):
    content = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False,
                                               layout_mode_scale_weight=2.0, )
    lines = content.split("\n")
    resultSet = list()
    for line in lines:
        if(line.startswith("    ")): #Either a heading or conclusion
            continue
        data_array = [e.strip() for e in re.split(r"\s{4,}", line.strip())]
        if(len(data_array) == 5):
            inc = Incident(data_array[0], data_array[1], data_array[2], data_array[3], data_array[4])
            resultSet.append(inc)
        elif(len(data_array) == 3):
            inc = Incident(data_array[0], data_array[1], "", "", data_array[2])
            resultSet.append(inc)
    return resultSet


def connectAndTestDB():
    sqliteConn = sqlite3.connect(db_location)
    sqlCursor = sqliteConn.cursor()
    sqlCursor.execute(drop_query) # First drop the data
    sqlCursor.execute(create_query) #Create table again
    result = sqlCursor.execute(count_incidents_query) # Count incidents query, to check if table has been created
    return sqliteConn


def insertResultSet(incidents, conn):
    cursor = conn.cursor()
    cursor.executemany(sql_insert, [(incident.incident_time, incident.incident_number,incident.incident_location, incident.nature, incident.incident_ori) for incident in incidents])
    conn.commit()
    cursor.execute("select count(*) from incidents")
    result = cursor.fetchall()
    cursor.close()


def natureTypeState(conn):
    cursor = conn.cursor()
    cursor.execute(nature_type_query)
    result = cursor.fetchall()
    cursor.close()
    return result



if __name__ == '__main__':
    s = os.environ["PATH"].split(';')
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                         help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        parseUrl(args.incidents)
