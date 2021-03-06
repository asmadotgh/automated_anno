import pandas as pd
import os
import requests



# python personalized_email/get_names.py
# alternatively, ldapsearch -x -H ldaps://ldap.mit.edu -b ou=moira,dc=mit,dc=edu uid=<kerberos> looping over kerberos
if __name__ == "__main__":
    df = pd.read_csv(os.path.join('data', 'ashdown_mailinglist.txt'), sep="\n", header=None)
    num_users = len(df)

    def retrieve_name(series):
        series['kerberos'] = series['email'][:series['email'].find('@mit.edu')]
        try:
            r = requests.get('https://web.mit.edu/bin/cgicso?options=general&query={}'.format(series['kerberos']))
            two_matches = r.text.find('There were 2 matches to your request.') >= 0
            found = r.text.find('No matches to your query') == -1
            if two_matches or not found:
                return series

            start = r.text.find('name: ')
            end = r.text.find('\n     email: ')
            name_str = r.text[start+len('name: '):end]
            comma = name_str.find(', ')
            series['lastname'] = name_str[:comma]
            series['firstname'] = name_str[comma + len(', '):]
        except:
            print('Error while retrieving user {}'.format(series['kerberos']))
        finally:
            print('\x1b[1A\x1b[2K{}/{} done'.format(int(series.name) + 1, num_users))
            return series
    df.columns = ["email"]
    df = df.apply(retrieve_name, axis=1)
    df.to_csv(os.path.join('data', 'processed_mailinglist.csv'), header=True)
