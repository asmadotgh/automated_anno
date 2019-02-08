# Automated Announcement Generation
This code automatically sends announcement emails to Ashdown community based on the event list from the designated spreadsheet.

## Usage
pip install -r requirements.txt
python main.py [--start_date=<YYYY-MM-DD> --from_email=<from> --to_email=<to>]

\<YYYY-MM-DD> is the starting date. It is optional. If not specified then anno will be generated for a week from today.

\<from> is an optional email address ending in @mit.edu. If not set, the default value will be used.

\<to> is an optional email address ending in @mit.edu. If not set, the default value will be used.

## Note
The code has been tested with python 3.6.
 
#### Setting up the automatic email sending from gmail
https://stackabuse.com/how-to-send-emails-with-gmail-using-python/

#### Setting up sheets API 
https://developers.google.com/sheets/api/quickstart/python?authuser=3


