import pandas as pd
import os

# python personalized_email/merge_data.py
if __name__ == "__main__":
    df1 = pd.read_csv(os.path.join('data', 'processed_mailinglist.csv'))
    df2 = pd.read_csv(os.path.join('data', 'Roster for Madeleine.csv'), header=None)
    df2.columns = ['room_number', 'firstname', 'lastname', 'gender']
    merged_df = pd.merge(df1, df2, on=['firstname', 'lastname'], how='outer') # how='right'
    # df3 = pd.read_csv(os.path.join('data', 'processed_retrieved_emails_bu.csv'))
    # merged_df = pd.merge(df1, df3, on=['kerberos'], how='right')
    merged_df.to_csv(os.path.join('data', 'merged_emails.csv'))
    print(merged_df)
