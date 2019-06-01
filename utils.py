import datetime as dt
import logging
import sys
import re

class Utils:

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1WLVTQtwsCHL1uAG5nFK0u7YN2qtzV1iOyvOGOFHM024'
    RANGE_NAME = 'Form Responses!B2:H'

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

    FROM_EMAIL = 'ashdown-anno@mit.edu'
    FROM_PASS = 'REPLACE WITH PASS'
    CURR_DATE = dt.date.today().strftime(DATE_FORMAT)
    DURATION = '1W'     # '?W', '?M', '?D', 'ALL'
    TO_EMAIL = 'ashdown-anno@mit.edu'    # 'asma_gh@mit.edu'
    LOGS_EMAIL = 'ashdown-anno@mit.edu'  # 'asma_gh@mit.edu'

    @staticmethod
    def is_valid_date(inp):
        try:
            dt.datetime.strptime(inp, Utils.DATE_FORMAT)
            return True
        except:
            logging.warning(
                'Error. Date needs to follow ' + Utils.INLINE_DATE_FORMAT + ' format. ' + str(sys.exc_info()[0]))
            return False

    @staticmethod
    def is_valid_time(inp):
        try:
            dt.datetime.strptime(inp, Utils.TIME_FORMAT)
            return True
        except:
            logging.warning(
                'Error. Time needs to follow ' + Utils.INLINE_TIME_FORMAT + ' format. ' + str(sys.exc_info()[0]))
            return False

    @staticmethod
    def get_duration_time_delta(duration_inp):
        duration = duration_inp.lower()

        try:

            # All events in the future
            if duration == 'all':
                print(f'Processing all events in the future.')
                return dt.timedelta(weeks=1000)

            # x Weeks
            week_r = re.compile('.*w')
            if week_r.match(duration) is not None:
                x = int(duration[:-1])
                print(f'Processing {x} weeks into the future.')
                return dt.timedelta(weeks=x)

            # x Days
            day_r = re.compile('.*d')
            if day_r.match(duration) is not None:
                x = int(duration[:-1])
                print(f'Processing {x} days into the future.')
                return dt.timedelta(days=x)

            # x Months
            month_r = re.compile('.*m')
            if month_r.match(duration) is not None:
                x = int(duration[:-1])
                print(f'Processing {x} months into the future.')
                return dt.timedelta(days=x*30)
        except:
            logging.error('Error. Duration needs to be in <?D/W/M> or ALL format. ' + str(sys.exc_info()[0]))
            dt.timedelta(days=7)

    @staticmethod
    def is_valid_image_format(inp):
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        for ext in valid_extensions:
            if inp.endswith(ext):
                return True
        logging.warning('Error. Image extension not supported. '
                        'Please use jpg, png, or gif. If you intend to use pdf, use the url in the text.')

    @staticmethod
    def is_valid_email(inp):
        if Utils.EMAIL_REGEX.match(inp):
            return True
        logging.warning('Error. Invalid email: '+inp)
        return False
