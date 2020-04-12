import pandas as pd
import os

# python personalized_email/remove_officers.py
if __name__ == "__main__":
    all_residents = pd.read_csv(os.path.join('data', 'roster_retrieved_emails_postprocessed.csv'), index_col=0)
    officers = pd.read_csv(os.path.join('data', 'officers.txt'), header=None)
    exclude = pd.read_csv(os.path.join('data', 'exclude.txt'), header=None)
    exclude = pd.concat([officers, exclude])
    exclude.columns = ['kerberos']

    output_df = all_residents.loc[pd.merge(all_residents, exclude, on=['kerberos'], how='left', indicator=True)['_merge'] == 'left_only']
    output_df.to_csv(os.path.join('data', 'all_but_officers_and_exclusions.csv'))
    print(output_df)
