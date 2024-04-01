import sqlite3
import pytest
import requests

from unittest.mock import Mock
from assignment0 import main


class MockPageObject:
    def __init__(self, content):
        self.content = content

    def extract_text(self, extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=2.0):
        return self.content


def test_parseUrl():
    with pytest.raises(requests.exceptions.MissingSchema):
        main.parseUrl("sample")


def test_database():
    obj = main.connectAndTestDB()
    assert isinstance(obj, sqlite3.Connection)
    print("Test2 runs")


def test_parseAndFetchResults():
    with pytest.raises(requests.exceptions.MissingSchema):
        main.parseUrl("sampleUrl")


def test_parseEachPage():
    page_content = "Some text\n Data1    Data2    Data3    Data4    Data5\n"
    page_object = MockPageObject(page_content)
    result_set = main.parseEachPage(page_object)


    assert len(result_set) == 1
    assert isinstance(result_set[0], main.Incident)
    assert result_set[0].incident_time == "Data1"
    assert result_set[0].incident_number == "Data2"
    assert result_set[0].incident_location == "Data3"
    assert result_set[0].nature == "Data4"
    assert result_set[0].incident_ori == "Data5"

def test_insertResultSet():
    # Mock cursor
    mock_cursor = Mock()
    mock_conn = Mock()
    mock_conn.cursor.return_value = mock_cursor
    incidents = [
        main.Incident("2022-01-01", "123", "Location1", "Nature1", "Ori1"),
        main.Incident("2022-01-02", "124", "Location2", "Nature2", "Ori2"),
        main.Incident("2022-01-03", "125", "Location3", "Nature3", "Ori3"),
    ]
    main.insertResultSet(incidents, mock_conn)
    mock_cursor.executemany.assert_called_once()

def test_natureTypeState():
    mock_cursor = Mock()
    mock_conn = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_result = [("Nature1", 10), ("Nature2", 15), ("Nature3", 5)]
    mock_cursor.fetchall.return_value = mock_result

    results = main.natureTypeState(mock_conn)

    assert mock_result == results
