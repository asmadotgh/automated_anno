import pandas as pd
import os
import requests


# python get_names.py
if __name__ == "__main__":
    df = pd.read_csv(os.path.join('data', 'ashdown_mailinglist.txt'), sep="\n", header=None)
    num_users = len(df)

    def retrieve_name(series):
        series['kerboras'] = series['email'][:series['email'].find('@mit.edu')]
        try:
            r = requests.get('https://web.mit.edu/bin/cgicso?options=general&query={}'.format(series['kerboras']))
            found = r.text.find('No matches to your query') == -1
            if found:
                start = r.text.find('name: ')
                end = r.text.find('\n     email: ')
                name_str = r.text[start+len('name: '):end]
                comma = name_str.find(', ')
                series['lastname'] = name_str[:comma]
                series['firstname'] = name_str[comma + len(', '):]
        except:
            print('Error while retrieving user {}'.format(series['kerboras']))
        finally:
            print('\x1b[1A\x1b[2K{}/{} done'.format(int(series.name) + 1, num_users))
            return series
    df.columns = ["email"]
    df = df.apply(retrieve_name, axis=1)
    df.to_csv(os.path.join('data', 'processed_mailinglist.csv'), header=True)
