import os
import sqlite3
import pytest
from project0 import main


@pytest.fixture
def test_db():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents 
        (incident_time TEXT, 
        incident_number TEXT, 
        incident_location TEXT, 
        nature TEXT, 
        incident_ori TEXT);''')
    db.commit()
    yield db
    db.close()

def test_createdb():
    conn = project0.createdb()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    assert cursor.fetchone() is not None, "Table 'incidents' should be created"
    conn.close()

def test_populatedb(test_db):
    incidents = [
        {'Date/Time': '10/31/2024 23:59', 'Incident Number': '2024-00001313', 'Location': 'ELM ST', 'Nature': 'Ghost Sighting', 'Incident ORI': 'OK1234567'},
        {'Date/Time': '10/31/2024 00:00', 'Incident Number': '2024-00006666', 'Location': 'CRYSTAL LAKE', 'Nature': 'Slasher Attack', 'Incident ORI': 'EMSSTAT'}
    ]
    
    project0.populatedb(test_db, incidents)
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM incidents;")
    rows = cursor.fetchall()
    
    assert len(rows) == 2, "Two incidents should be in the table"
    assert rows[0][1] == '2024-00001313', "Incident number should match '2024-00001313'"
    assert rows[1][3] == 'Slasher Attack', "Second incident should be 'Slasher Attack'"

def test_status(test_db, capsys):
    mock_incidents = [
        {'Date/Time': '10/31/2024 23:59', 'Incident Number': '2024-00001313', 'Location': 'Elm Street', 'Nature': 'Ghost Sighting', 'Incident ORI': 'OK1234567'},
        {'Date/Time': '10/31/2024 00:00', 'Incident Number': '2024-00006666', 'Location': 'Crystal Lake', 'Nature': 'Slasher Attack', 'Incident ORI': 'EMSSTAT'},
        {'Date/Time': '10/30/2024 03:00', 'Incident Number': '2024-00009999', 'Location': 'Camp Crystal Lake', 'Nature': 'Slasher Attack', 'Incident ORI': 'OK7654321'}
    ]

    project0.populatedb(test_db, mock_incidents)

    project0.status(test_db)

    captured = capsys.readouterr()

    expected_output = (
        "Ghost Sighting|1\n"
        "Slasher Attack|2\n"
    )

    assert captured.out == expected_output, f"Expected output: {expected_output}, Error: {captured.out}"
