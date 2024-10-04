import os
from project0.incident_parser import extractincidents
from pypdf import PdfReader
import pytest

def test_extractincidents():
    test_pdf_path = os.path.join("docs", "2024-08-05_daily_incident_summary.pdf")
    
    with open(test_pdf_path, "rb") as f:
        pdf_data = f.read()
    
    
    incidents = extractincidents(pdf_data)
    print(len(incidents))
    assert len(incidents) == 407, "Incorrect number of incidents."
    reader = PdfReader(test_pdf_path)
    total_pages = len(reader.pages)
    assert total_pages == 25, f"Incorrect number of pages."
    #first one
    first_incident = incidents[0]
    
    assert first_incident['Date/Time'] == '8/5/2024 0:03', "Wrong"
    assert first_incident['Incident Number'] == '2024-00056396', "Wrong"
    assert first_incident['Location'] == '318 E HAYES ST', "Wrong"
    assert first_incident['Nature'] == 'Trespassing', "Wrong"
    assert first_incident['Incident ORI'] == 'OK0140200', "Wrong"
    
    print(f"Extracted incident: {first_incident}")
    
    # Try a random one with an edge case
    target_incident = next((i for i in incidents if i['Incident Number'] == '2024-00056658'), None)
    assert target_incident is not None, "Wrong"
    
    assert target_incident['Date/Time'] == '8/5/2024 22:20', "Wrong"
    assert target_incident['Incident Number'] == '2024-00056658', "Wrong"
    assert target_incident['Location'] == '35.1809766666667;-97.4160433333333', "Wrong"
    assert target_incident['Nature'] == 'Contact a Subject', "Wrong"
    assert target_incident['Incident ORI'] == 'OK0140200', "Wrong"
    print(f"Extracted incident 2024-00056658: {target_incident}")
    
    # Last one    
    last_incident = incidents[-1]
    assert last_incident is not None, "Wrong"
    assert last_incident['Date/Time'] == '8/5/2024 23:58', "Wrong"
    assert last_incident['Incident Number'] == '2024-00056678', "Wrong"
    assert last_incident['Location'] == '1171 W BOYD ST', "Wrong"
    assert last_incident['Nature'] == 'Traffic Stop', "Wrong"
    assert last_incident['Incident ORI'] == 'OK0140200', "Wrong"
    print(f"Extracted incident 2024-00056678: {last_incident}")