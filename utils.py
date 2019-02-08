import datetime as dt
import logging
import sys

class Utils:

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1WLVTQtwsCHL1uAG5nFK0u7YN2qtzV1iOyvOGOFHM024'
    RANGE_NAME = 'Sheet1!A3:F'

    DATE_FORMAT = '%Y-%m-%d'
    HUMAN_READABLE_DATE_FORMAT = '%b %d, %Y'

    TIME_FORMAT = '%H:%M'
    HUMAN_READABLE_TIME_FORMAT = '%I:%M %p'

    EMAIL_POSTFIX = '@mit.edu'

    SPREADSHEET_STARTING_ROW = 3

    def is_valid_date(inp):
        try:
            dt.datetime.strptime(inp, Utils.DATE_FORMAT)
            return True
        except:
            logging.warning('Error. Date needs to follow YYYY-MM-DD format. ' + str(sys.exc_info()[0]))
            return False

    def is_valid_time(inp):
        try:
            dt.datetime.strptime(inp, Utils.TIME_FORMAT)
            return True
        except:
            logging.warning('Error. Time needs to follow HH-MM format. ' + str(sys.exc_info()[0]))
            return False
    def is_valid_image_format(inp):
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        for ext in valid_extensions:
            if inp.endswith(ext):
                return True
        logging.warning('Error. Image extension not supported. '
                        'Please use jpg, png, or gif. If you intend to use pdf, use the url in the text.')