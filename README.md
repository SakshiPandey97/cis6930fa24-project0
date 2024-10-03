# cis6930fa24-project0

How to Use with pipenv:

1. Install pipenv if not already present and activate the pipenv shell environment.

pip install pipenv

pipenv shell

2. Clone the repository from GitHub or download the script and unzip it to the directory where you would like to create your db.
git clone <repository_url>

3.To run the script you need to provide the URL of the incident PDF file you want to download and process following the --incidents flag. This script was designed to be used to process incident reports from the Norman Police Department. This is an example use of the script:

pipenv run python main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-05_daily_incident_summary.pdf
