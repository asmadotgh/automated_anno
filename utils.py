import datetime as dt
import logging
import sys
import re

class Utils:

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1WLVTQtwsCHL1uAG5nFK0u7YN2qtzV1iOyvOGOFHM024'
    RANGE_NAME = 'Form Responses!B2:G'

    # DATE_FORMAT = '%Y-%m-%d'
    DATE_FORMAT = '%m/%d/%Y'
    INLINE_DATE_FORMAT = 'MM/DD/YYYY'
    HUMAN_READABLE_DATE_FORMAT = '%b %d, %Y'

    # TIME_FORMAT = '%H:%M'
    TIME_FORMAT = '%I:%M:%S %p'
    INLINE_TIME_FORMAT = 'HH:MM:SS AM/PM'
    HUMAN_READABLE_TIME_FORMAT = '%I:%M %p'

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    SPREADSHEET_STARTING_ROW = 2

    FROM_EMAIL = 'ashdown.anno@gmail.com'
    FROM_PASS = 'tdyQm886QcwAZQS'
    CURR_DATE = dt.date.today().strftime(DATE_FORMAT)
    TO_EMAIL = 'asma_gh@mit.edu'  # ashdown-anno@mit.edu

    def is_valid_date(inp):
        try:
            dt.datetime.strptime(inp, Utils.DATE_FORMAT)
            return True
        except:
            logging.warning(
                'Error. Date needs to follow ' + Utils.INLINE_DATE_FORMAT + ' format. ' + str(sys.exc_info()[0]))
            return False

    def is_valid_time(inp):
        try:
            dt.datetime.strptime(inp, Utils.TIME_FORMAT)
            return True
        except:
            logging.warning(
                'Error. Time needs to follow ' + Utils.INLINE_TIME_FORMAT + ' format. ' + str(sys.exc_info()[0]))
            return False

    def is_valid_image_format(inp):
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        for ext in valid_extensions:
            if inp.endswith(ext):
                return True
        logging.warning('Error. Image extension not supported. '
                        'Please use jpg, png, or gif. If you intend to use pdf, use the url in the text.')

    def is_valid_email(inp):
        if Utils.EMAIL_REGEX.match(inp):
            return True
        logging.warning('Error. Invalid email: '+inp)
        return False