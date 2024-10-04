# cis6930fa24-project0 By: Sakshi Pandey
## Basic Premise
The purpose of this project is to automatically fetch, extract, and allow the user analyze daily incident summaries from the Norman Police Department. The software parses relevant incident details such as Date/Time, Incident Number, Location, Nature, and Incident ORI, and stores them in a SQLite database. The database is then queried to obtain the count of different types of incidents.

This project is designed to ensure accurate data extraction while handling the challenges of unstructured PDF data(specifically Norman PD's), and it maintains data integrity by resetting the database on every run.
## Video Demo
<!-- Embed YouTube Video -->
<a href="https://youtu.be/Kh1HKSH_rCw" target="_blank">
  <img src="https://img.youtube.com/vi/Kh1HKSH_rCw/0.jpg" alt="Watch the video" style="width:100%;"/>
</a>

## Potential Use-Cases
We could use this to turn messy PDF reports into clean, structured data, making it easy to store and pull up whenever needed. It would also be great for creating visual dashboards or charts to track crime patterns and see trends over time, helping people keep an eye on incidents in specific areas.
Some Specific Areas of Use:
- Public Safety Data Analytics
- Criminal Research
- Improved Record Keeping for Police Departments

## Overview of Functionality
Fetching PDF Data(fetchincidents):
The system begins by retrieving incident summary PDF files from a specified URL. It uses an HTTP request with custom headers to mimic a browser and download the file.
The fetchincidents() function handles any possible HTTP 404 errors (file not found) or 500 error, ensuring that if the file cannot be retrieved, a clear error message is returned.

Extracting Incident Information(extractincidents):
The extractincidents() function processes the downloaded PDF to extract important details like Date/Time, Incident Number, Location, Nature, and Incident ORI.
It reads the PDF page by page, splitting the content into lines. It skips over irrelevant lines, such as headers or empty lines. For each valid line, it splits the text into parts and organizes the data into a structured format.
Finally, the function returns a list of all the extracted incidents.

Database Creation and Management(createdb):
After extracting the incidents, the system creates a SQLite database, normanpd.db, to store the structured data.
The createdb() function first checks if an existing database file is present and deletes it to ensure the results from previous runs do not interfere with the current data. This guarantees that only the most recent incident data is included in the analysis.
It then creates a table with columns corresponding to the extracted fields: incident_time, incident_number, incident_location, nature, and incident_ori.

Populating the Database(populatedb):
Once the database is created, the parsed incident data is inserted into the SQLite database using the populatedb() function.
Each incident’s Date/Time, Incident Number, Location, Nature, and Incident ORI are stored in the respective columns of the database.
This step transforms the unstructured data from the PDF into a structured database, allowing for easy retrieval and analysis.

Incident Analysis(status):
The status function queries the database to count the number of incidents grouped by their Nature (e.g., Trespassing, Assauly, Haunting etc.). This provides a clear summary of the types of incidents reported, offering insights into the most common or concerning issues.
The results are then printed, allowing users to see a summary of the incidents and incident numbers, organized by category, for further analysis.

## How to Use with pipenv:
1. Install python3(version 3.10) if you don't have it already.
2. **Install pipenv if not already present and activate the pipenv shell environment.**

```bash
pip install pipenv
pipenv shell
```
3. Clone the repository from GitHub or download the script and unzip it to the directory where you would like to create your db.
```
git clone git@github.com:SakshiPandey97/cis6930fa24-project0.git
```
4. To run the script you need to provide the URL of the incident PDF file you want to download and process following the --incidents flag. This script was designed to be used to process incident reports from the Norman Police Department. This is an example use of the script:
```
pipenv run python main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-05_daily_incident_summary.pdf
```
## Design Decisions
1. The PDF is temporarily saved to /tmp/downloaded_file.pdf before processing. While efficient for this project, in real-world applications, it may be necessary to store the PDF files long-term for record-keeping especially since normanpd might delete files.
2. In this project, the database (normanpd.db) is deleted and recreated each time the code is executed. This design choice ensures that the data printed from the database reflects only the most recent run, preventing old or outdated incident records from influencing the output.
3. The code assumes that if an incident spans multiple lines and the line has fewer than 5 parts (ex. It doesn't follow the expected pattern of Date/Time, Incident Number, Location, Nature, Incident ORI), the line is always part of the Location. This might be problematic if other fields (like Nature) also span multiple lines, as the code currently appends these lines to Location without verifying if it's indeed location data. However I feel this assumption is reasonable following manually looking at various pdf reports. Nature is always concise and summarized in 2-3 words. I had initially tried adding additional check with common words such as Ave or St but I feel this solution is clean and decided not to include those checks. 
4. The code assumes that the layout of the incident PDF files will remain consistent, specifically relying on fixed patterns such as headers. It assumes that each incident follows a similar structure (Date/Time, Incident Number, Location, Nature, and Incident ORI). Therefore, the code depends on splitting lines into exactly 5 parts using multiple spaces (\s{2,}). If the PDF structure changes significantly, the extraction process would break.
5.  The code skips over empty lines and lines that only contain dates without incident details to avoid processing irrelevant data. It uses a regex pattern to match lines that are just dates and skips them. The regex pattern (r"^\d{1,2}/\d{1,2}/\d{4}(\s+\d{1,2}:\d{2})?$") assumes that dates follow the format MM/DD/YYYY and that the time (if present) is in HH:MM format. If this isn't followed then parsing and removing the last line of the pdf(which has only Date / Time and no incident) fails.

## Tests
3 Test Cases were used to test this software they individually test each function in the incident_parser.py:
1. test_fetchincidents.py: Two tests are carried out here. The first test mocks a successful HTTP response and verifies that the fetched data matches the expected result. The second test simulates an HTTP 404 error to ensure the function handles it correctly by returning None.
2. test_extract.py: This test checks if the system correctly extracts incidents from a PDF. It verifies the total number of incidents, validates the details of the first, a random, and the last incident, ensuring all data is parsed correctly.
3. test_db.py: This test checks if the database is correctly created, populated, and if the status() function outputs the correct incident summary. 
