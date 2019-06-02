# Automated Announcement Generation
This code automatically sends announcement emails to Ashdown community based on the event list from the designated spreadsheet.

## Note
The code has requires Python 3.6+. It has been tested on 3.6.8.

## Setup
1. Run the following command to install the necessary python libraries:

`pip install -r requirements.txt`

2. Download `token.json` that has been shared with you in the root directory of this repository. 


## Usage
python main.py [--start_date=\<MM/DD/YYYY>  --duration=\<?{D/W/M}/ALL> --from_email=\<from> --from_pass=\<pass> --to_email=\<to> --logs_email=\<cc>]

\<MM/DD/YYYY> is the starting date. It is optional. If not specified then anno will be generated for a week from today.

\<X{D/W/M}/ALL> is how far ahead the anno is considering events. It can be identified in terms of 
number of X number of days, weeks, months, or everything in the future. 
Examples: 5D = 5 days in the future, 2W = 2 weeks in the future, 1M = 1 month ahead, ALL = all future events 

\<from> is the from email address. The default is ashdown-anno [at] mit.

\<to> is the to email address. The default value is ashdown-anno [at] mit.

\<cc> is the email address to send log files to, i.e. success or failure of sending emails. The default value is ashdown-anno [at] mit.


 
#### Setting up the automatic email sending from gmail
https://stackabuse.com/how-to-send-emails-with-gmail-using-python/

#### Setting up sheets API 
https://developers.google.com/sheets/api/quickstart/python?authuser=3


