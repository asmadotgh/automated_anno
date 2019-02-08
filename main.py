"""
Main function to automate sending announcements.
Input: sender and receiver email. The starting date from which a week is considered.
Output: sends email to the receiver email set above.
"""

#TODO: p0 document usage in the Ashdown wiki
#TODO: p0 after properly testing, clone scripts on server and schedule a cron job

import logging
import datetime as dt
import argparse
from utils import Utils
from logging_config import *
from create_email import create_email

from_email = 'asma_gh@mit.edu'
curr_date = dt.date.today().strftime(Utils.DATE_FORMAT)
to_email = 'asma_gh@mit.edu'


def is_valid_email(inp):
    if inp.endswith(Utils.EMAIL_POSTFIX):
        return True
    logging.warning('Error. Email needs to end with ' + Utils.EMAIL_POSTFIX)
    return False


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--from_email', type=str,
                           default=from_email,
                           required=False,
                           help="<from> is an optional email address ending in @mit.edu."
                                "If not set, the default value will be used")
    argparser.add_argument('--start_date', type=str, default=curr_date,
                           help="<YYYY-MM-DD> is the starting date. It is optional."
                                "If not specified then anno will be generated for a week from today.")
    argparser.add_argument('--to_email', type=str, default=to_email,
                           help="<to> is an optional email address ending in @mit.edu."
                                "If not set, the default value will be used.")
    args = argparser.parse_args()

    # logging.basicConfig(filename='main.log', level=logging.DEBUG)
    logging.info('Creating newsletter ...')
    logging.info('Usage: python main.py [--from_email=<from> --start_date=<YYYY-MM-DD> --to_email=<to>]')

    #TODO: check if the date is plausible?

    is_valid = is_valid_email(args.from_email) and is_valid_email(args.to_email) and Utils.is_valid_date(
        args.start_date)
    if is_valid:
        create_email(args.from_email, args.start_date, args.to_email)
    else:
        logging.error('Aborting... Usage: '
                      'python main.py [--from_email=<from> --start_date=<YYYY-MM-DD> --to_email=<to>]')


