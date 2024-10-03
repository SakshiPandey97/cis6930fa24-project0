# cis6930fa24-project0

## How to Use with pipenv:

1. **Install pipenv if not already present and activate the pipenv shell environment.**

```bash
pip install pipenv
pipenv shell
```
2. Clone the repository from GitHub or download the script and unzip it to the directory where you would like to create your db.
```
git clone git@github.com:SakshiPandey97/cis6930fa24-project0.git
```
3. To run the script you need to provide the URL of the incident PDF file you want to download and process following the --incidents flag. This script was designed to be used to process incident reports from the Norman Police Department. This is an example use of the script:
```
pipenv run python main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-05_daily_incident_summary.pdf
```
## Design Decisions
Temporary File for PDF Processing:
The PDF is temporarily saved to /tmp/downloaded_file.pdf before processing. While efficient for this project, in real-world applications, it may be necessary to store the PDF files long-term for record-keeping and audits.

# Edge Case Handling:
Handling "911" in Location vs. Nature: A specific edge case occurs with the "911" keyword. In some reports, "911" is part of the location, while in others, it's part of the nature of the incident. To resolve this, a custom hard-coded solution ensures that "911" is correctly attributed based on context:
For example:
911 W MAIN ST Welfare Check: Here, 911 is part of the location, and the nature is Welfare Check.
911 Call Nature Unknown: Here, 911 is part of the nature, not the location.

EMSSTAT and 14005 in Case Number: These are special ORI identifiers used for emergency medical services. The script treats these as valid ORI values and processes them accordingly.
Dealing with Uppercase and Lowercase Words in Nature:

Basic Premise

Potential Use-Cases

Overview of Functionality

Additional Notes and Details
emstat and 14005 in casenumber
2024-08-01 - 2024-08-06 I looked at these manually.

Regex pattern to detect nature of incidents:
Matches "MVA", "COP", "911" (all uppercase or numeric patterns)
Matches capitalized words followed by lowercase letters (e.g., "Traffic")
Matches combinations like "Assault/Robbery" where two capitalized words are separated by a slash

I delete the db if it already exists in my code. 

although tmp efficient for this project should we keep records irl?
