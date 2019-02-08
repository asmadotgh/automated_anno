# Automated Announcement Generation
This code automatically sends announcement emails to Ashdown community based on the event list from the designated spreadsheet.

## Usage
python main.py [--from_email=<from> --start_date=<YYYY-MM-DD> --to_email=<to>]

\<from> is an optional email address ending in @mit.edu. If not set, the default value will be used.

\<YYYY-MM-DD> is the starting date. It is optional. If not specified then anno will be generated for a week from today.

\<to> is an optional email address ending in @mit.edu. If not set, the default value will be used.
