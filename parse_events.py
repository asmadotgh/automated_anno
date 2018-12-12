'''
Parsing a google spreadsheet into a dataframe composing of relevant events.
'''

import pandas as pd
import datetime as dt
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from my_constants import MyConstants

def timely(inp_date_str, start_date_str):
    inp_date = dt.datetime.strptime(inp_date_str, MyConstants.DATE_FORMAT)
    start_date = dt.datetime.strptime(start_date_str, MyConstants.DATE_FORMAT)
    end_date = dt.datetime.strptime(start_date_str, MyConstants.DATE_FORMAT) + dt.timedelta(days=7)
    return inp_date >= start_date and inp_date <= end_date

def parse_events(curr_date):
    df = pd.DataFrame(columns=['title', 'date', 'time', 'location', 'description', 'image'])

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', MyConstants.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=MyConstants.SPREADSHEET_ID,
                                range=MyConstants.RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            if not timely(row[1], curr_date):
                continue
            df = df.append(
                pd.Series(data={'title': row[0], 'date': row[1], 'time': row[2],
                                'location': row[3], 'description': row[4], 'image': row[5] if len(row) > 5 else None}),
                ignore_index=True)

    df.sort_values(by=['date', 'time'], inplace=True)
    return df
