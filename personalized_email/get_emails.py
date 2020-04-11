import pandas as pd
import numpy as np
import os
import requests


# python personalized_email/get_emails.py
if __name__ == "__main__":
    df = pd.read_csv(os.path.join('data', 'Roster for Madeleine.csv'), header=None)
    df.columns = ['room_number', 'firstname', 'lastname', 'gender']
    num_users = len(df)

    def retrieve_email(series):
        try:
            r = requests.get('https://web.mit.edu/bin/cgicso?options=general&query={} {}'.format(series['firstname'], series['lastname']))
            unknown_email = r.text.find('email: Unknown') >= 0
            other_error = r.text.find('Too many entries to print -') >= 0
            multiple_matches = False
            for i in np.arange(2, 10):
                if r.text.find('There were {} matches to your request.'.format(i)) >= 0:
                    multiple_matches = True
            found = r.text.find('No matches to your query') == -1

            if unknown_email or multiple_matches or other_error or not found:
                return series

            start = r.text.find('@MIT.EDU">')
            end = r.text.find('@MIT.EDU</A>')
            kerberos = r.text[start+len('@MIT.EDU">'):end]
            series['kerberos'] = kerberos
            series['email'] = kerberos + '@mit.edu'
        except:
            print('Error while retrieving user {} {}'.format(series['firstname'], series['lastname']))
        finally:
            print('\x1b[1A\x1b[2K{}/{} done'.format(int(series.name) + 1, num_users))
            return series
    df = df.apply(retrieve_email, axis=1)
    df.to_csv(os.path.join('data', 'processed_retrieved_emails_bu.csv'), header=True)
