"""
Parsing a google spreadsheet into a dataframe composing of relevant events.
"""

import pandas as pd
import datetime as dt
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from logging_config import *


def timely(inp_date_str, start_date_str, duration):
    inp_date = dt.datetime.strptime(inp_date_str, Utils.DATE_FORMAT)
    start_date = dt.datetime.strptime(start_date_str, Utils.DATE_FORMAT)
    end_date = dt.datetime.strptime(start_date_str, Utils.DATE_FORMAT) + duration
    return (inp_date >= start_date) and (inp_date <= end_date)


def parse_events(curr_date, duration):
    df = pd.DataFrame(columns=['title', 'date', 'start_time', 'end_time', 'location', 'description', 'image'])

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', Utils.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=Utils.SPREADSHEET_ID,
                                range=Utils.RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        logging.warning('No data found.')
    else:
        for idx, row in enumerate(values):
            necessary_cols = [0, 1, 2, 4, 5]
            missing_necessary_col = False
            if len(row) < 6:
                missing_necessary_col = True
            else:
                for i in necessary_cols:
                    if not row[i]:
                        missing_necessary_col = True
            if missing_necessary_col:
                logging.warning(
                    'Missing necessary values: event name, date, start time, location, description. Skipping row ' + str(
                        idx + Utils.SPREADSHEET_STARTING_ROW) + '.')
                continue
            if not Utils.is_valid_date(row[1]):
                logging.warning(
                    'Incorrect date format. Skipping row ' + str(idx + Utils.SPREADSHEET_STARTING_ROW) + '.')
                continue
            if not timely(row[1], curr_date, duration):
                logging.warning('Date not in range. Skipping row ' + str(idx + Utils.SPREADSHEET_STARTING_ROW) + '.')
                continue
            if not Utils.is_valid_time(row[2]):
                logging.warning(
                    'Incorrect time format. Skipping row ' + str(idx + Utils.SPREADSHEET_STARTING_ROW) + '.')
                continue
            df = df.append(
                pd.Series(data={'title': row[0], 'date': row[1], 'start_time': row[2], 'end_time': row[3],
                                'location': row[4], 'description': row[5], 'image': row[6] if len(row) > 6 else None}),
                ignore_index=True)

    df.sort_values(by=['date', 'start_time'], inplace=True)
    df = df.reset_index(drop=True)
    return df
