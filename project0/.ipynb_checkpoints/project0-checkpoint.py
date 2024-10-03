import urllib.request
from urllib.error import HTTPError
from pypdf import PdfReader
import re
import os
import sqlite3

def fetchincidents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    }
    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
        data = response.read()
        return data
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return None

def extractincidents(pdf_data):
    def clean_location(location, case_number, ori):
        location = location.replace(case_number, "").strip()
        location = location.replace(ori, "").strip()

        #Remove datetime patterns and the title
        date_time_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}")
        location = date_time_pattern.sub("", location).strip()
        location = location.replace("NORMAN POLICE DEPARTMENT", "").strip()
        #print(location)
        return location

    def extract_location_nature(location_text, case_number, ori):
        location_text = clean_location(location_text, case_number, ori)
        #Check for 911 or Traffic (capital and then lowercase) or / Assault
        nature_pattern = re.compile(r"(MVA|COP|911|[A-Z][a-z]+(?:/[A-Z][a-z]+)?)")
        
        location_parts = location_text.split()
        location = []
        nature = []
        is_nature = False

        for part in location_parts:
            if nature_pattern.match(part):  
                is_nature = True
                nature.append(part)
            elif not is_nature:  
                location.append(part)
            else:
                nature.append(part)

        location_str = ' '.join(location).strip()
        nature_str = ' '.join(nature).strip()
        

        if location:
            last_word = location[-1]
            #check for appended words when there are two lines in location
            split_index = None
            for i in range(len(last_word)):
                if last_word[i].isupper() and i + 1 < len(last_word) and last_word[i+1].islower():
                    split_index = i
                    break
            
            if split_index is not None:
                location_part = last_word[:split_index]
                nature_part = last_word[split_index:]

                location[-1] = location_part
                nature_str = f"{nature_part} {nature_str}".strip()
              
        #for edgecase on 8/05 bad solution and tedious
        nature_parts = nature_str.split()
        if nature_str.startswith("911") and len(nature_parts) > 1 and (len(nature_parts[1]) == 1 and nature_parts[1].isupper()) or (len(nature_parts) > 1 and nature_parts[1].isupper()):
            location_parts = []

            for i, part in enumerate(nature_parts):
                if part.isdigit() or part.isupper():
                    location_parts.append(part)
                else:
                    break

            location_str = f"{location_str} {' '.join(location_parts)}".strip()
            remaining_nature_parts = nature_parts[len(location_parts):]
            nature_str = ' '.join(remaining_nature_parts).strip()

        if not location_str:
            location_str = ' '.join(location_parts).strip()
        
        return ' '.join(location).strip(), nature_str

    pdf_file_path = '/tmp/downloaded_file.pdf'
    with open(pdf_file_path, 'wb') as temp_file:
        temp_file.write(pdf_data)
    
    with open(pdf_file_path, 'rb') as file:
        reader = PdfReader(file)

        date_time_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2})")
        case_number_pattern = re.compile(r"(2024-\d{8})")
        ori_pattern = re.compile(r"(OK\d{7}|EMSSTAT|14005)")

        incidents = []
        unique_incidents = set()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            if not text:
                continue

            entries = text.split('\n')
            incident = {}
            location_lines = []

            for entry in entries:
                entry = entry.strip()

                if not entry:
                    continue

                
                date_time = date_time_pattern.search(entry)
                if date_time:
                    if 'Date/Time' in incident and 'Incident Number' in incident:
                        if location_lines:
                            location_text = ' '.join(location_lines).strip()
                            incident['Location'], incident['Nature'] = extract_location_nature(location_text, incident['Incident Number'], incident.get('Incident ORI', ''))
                        incidents.append(incident)
                        incident = {}
                        location_lines = []  
                    incident['Date/Time'] = date_time.group(1)

                case_number = case_number_pattern.search(entry)
                if case_number:
                    incident['Incident Number'] = case_number.group(1)

                #get ORI or like EMSSTAT and 14005 
                #put in README
                ori = ori_pattern.search(entry)
                if ori:
                    incident['Incident ORI'] = ori.group(1)

                #get potential location and nature for further parsing
                if case_number or ori:
                    location_lines.append(entry)

            
            if 'Date/Time' in incident and 'Incident Number' in incident:
                if location_lines:
                    location_text = ' '.join(location_lines).strip()
                    incident['Location'], incident['Nature'] = extract_location_nature(location_text, incident['Incident Number'], incident.get('Incident ORI', ''))
                incidents.append(incident)

        return incidents

def createdb():
    home_db = "resources"
    db_path = os.path.join(home_db, "normanpd.db")
    #should I delete db if it already exists? we get wrong results in our status check otherwise
    #deleting the db to ensure that issue doesn't happen 
    if os.path.exists(db_path):
        os.remove(db_path)
    if not os.path.exists(home_db):
        os.makedirs(home_db)
    db_path = 'resources/normanpd.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents 
    (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);''')
    conn.commit()
    return conn

def populatedb(db, incidents):
    #print(incidents)
    cursor = db.cursor()
    
    for incident in incidents:
        cursor.execute('''INSERT INTO incidents(incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
        ''', (incident.get('Date/Time'), 
              incident.get('Incident Number'), 
              incident.get('Location'), 
              incident.get('Nature'), 
              incident.get('Incident ORI')))
    
    db.commit()

def status(db):
    cursor = db.cursor()
    cursor.execute('''
        SELECT nature, COUNT(*)
        FROM incidents
        WHERE nature IS NOT NULL AND nature != ''
        GROUP BY nature
        ORDER BY nature ASC;
    ''')
    rows = cursor.fetchall()

    for row in rows:
        nature, count = row
        print(f"{nature}|{count}")
