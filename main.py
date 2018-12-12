'''
Main function to automate sending announcements.
Input: sender and receiver email. The starting date from which a week is considered.
Output: sends email to the receiver email set above.
'''
import logging
import datetime as dt
from create_email import create_email

from my_constants import MyConstants
from logging_config import *

from_email = 'asma_gh@mit.edu'
curr_date = dt.date.today().strftime(MyConstants.DATE_FORMAT)
to_email = 'asma_gh@mit.edu'


def is_valid_email(inp):
    if inp.endswith(MyConstants.EMAIL_POSTFIX):
        return True
    logging.warning('Error. Email needs to end with '+MyConstants.EMAIL_POSTFIX)
    return False


def is_valid_date(inp):
    try:
        dt.datetime.strptime(inp, MyConstants.DATE_FORMAT)
        return True
    except:
        logging.warning('Error. Date needs to follow YYYY-MM-DD format. '+ str(sys.exc_info()[0]))
        return False


if __name__ == "__main__":
    # logging.basicConfig(filename='main.log', level=logging.DEBUG)
    # logging.config.dictConfig(config)
    logging.info('Creating newsletter ...')
    logging.info('Usage: \tpython main.py <from> <YYYY-MM-DD> <to>')
    logging.info('<from> is an optional email address ending in @mit.edu. If not set, the default value will be used.')
    logging.info('<YYYY-MM-DD> is the starting date. It is optional. If not specified then anno will be generated for a week from today.')
    logging.info('<to> is an optional email address ending in @mit.edu. If not set, the default value will be used.\n')

    #TODO: check if the date is plausible?

    if len(sys.argv) > 1:
        from_email = sys.argv[1]
    if len(sys.argv) > 2:
        curr_date = sys.argv[2]
    if len(sys.argv) > 3:
        to_email = sys.argv[3]
    is_valid = is_valid_email(from_email) and is_valid_email(to_email) and is_valid_date(curr_date)
    if is_valid:
        create_email(from_email, curr_date, to_email)
    else:
        logging.error('Aborting... Usage: \tpython main.py <from> <YYYY-MM-DD> <to>')


