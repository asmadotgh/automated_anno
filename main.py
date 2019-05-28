"""
Main function to automate sending announcements.
Input: sender and receiver email. The starting date and duration are for filtering the relevant events in the future.
Output: sends email to the receiver email set above.
"""

# TODO: p0 document usage in the Ashdown wiki

import logging
import datetime as dt
import argparse
from utils import Utils
from logging_config import *
from create_email import create_email


# Sample usage
# python main.py --start_date=02/08/2019 --duration=1W
if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--from_email', type=str,
                           default=Utils.FROM_EMAIL,
                           required=False,
                           help="<from> is an optional email address."
                                "The default setting uses " + Utils.FROM_EMAIL + ".")
    argparser.add_argument('--from_pass', type=str,
                           default=Utils.FROM_PASS,
                           required=False,
                           help="<from_pass> password for login.")
    argparser.add_argument('--start_date', type=str, default=Utils.CURR_DATE,
                           help="<" + Utils.INLINE_DATE_FORMAT + "> is the starting date. It is optional."
                                "If not specified then anno will be generated for a week from today.")
    argparser.add_argument('--duration', type=str, default=Utils.DURATION,
                           help="<?(D/W/M) or ALL> is the duration since the starting date. "
                                "It means ? days/weeks/months from start_date or including everything in the future, "
                                "respectively. If not specified, anno will be generated for a week from start_date.")
    argparser.add_argument('--to_email', type=str, default=Utils.TO_EMAIL,
                           help="<to> is an optional email address."
                                "If not set, the default value will be used.")
    argparser.add_argument('--covering', type=str, default='all',
                           help=".")
    args = argparser.parse_args()

    # logging.basicConfig(filename='main.log', level=logging.DEBUG)
    logging.info('Creating newsletter ...')
    logging.info(
        'Usage: python main.py [--start_date=<' + Utils.INLINE_DATE_FORMAT + '> --from_email=<from> --to_email=<to>]')

    is_valid = Utils.is_valid_email(args.from_email) and Utils.is_valid_email(args.to_email) and Utils.is_valid_date(
        args.start_date)
    if is_valid:
        create_email(args.from_email, args.from_pass, args.start_date, args.duration, args.to_email)
    else:
        logging.error(
            'Aborting... Usage: python main.py [--start_date=<' + Utils.INLINE_DATE_FORMAT + \
            '> --from_email=<from> --to_email=<to>]')


