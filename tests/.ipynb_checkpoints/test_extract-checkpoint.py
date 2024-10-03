import os
import main
import pytest

def test_extractincidents():
    test_pdf_path = os.path.join("docs", "2024-08-05_daily_incident_summary.pdf")
    
    with open(test_pdf_path, "rb") as f:
        pdf_data = f.read()
    
    
    incidents = main.project0.extractincidents(pdf_data)
    print(len(incidents))
    assert len(incidents) == 408, "Incorrect number of incidents."
    reader = main.project0.PdfReader(test_pdf_path)
    total_pages = len(reader.pages)
    assert total_pages == 25, f"Incorrect number of pages."
    
    #check first incident
    first_incident = incidents[0]
    
    assert first_incident['Date/Time'] == '8/5/2024 0:03', "Datetime value does not match"
    assert first_incident['Incident Number'] == '2024-00056396', "Incident Number does not match"
    assert first_incident['Location'] == '318 E HAYES ST', "Location value does not match"
    assert first_incident['Nature'] == 'Trespassing', "Nature does not match"
    assert first_incident['Incident ORI'] == 'OK0140200', "Incident ORI does not match"
    
    print(f"Extracted incident: {first_incident}")
    
    #try a random one with an edge case
    target_incident = next((i for i in incidents if i['Incident Number'] == '2024-00056658'), None)
    assert target_incident is not None, "Incident 2024-00056658 not found"
    
    assert target_incident['Date/Time'] == '8/5/2024 22:20', "Date/Time for 2024-00056658 does not match"
    assert target_incident['Incident Number'] == '2024-00056658', "Incident Number for 2024-00056658 does not match"
    assert target_incident['Location'] == '35.1809766666667;-97.4160433333333', "Location for 2024-00056658 does not match"
    assert target_incident['Nature'] == 'Contact a Subject', "Nature for 2024-00056658 does not match"
    assert target_incident['Incident ORI'] == 'OK0140200', "Incident ORI for 2024-00056658 does not match"
    print(f"Extracted incident 2024-00056658: {target_incident}")