"""
Putting events into a certain template, then creating and sending email.

Template:

[Ashdown] Ashdown-Anno for [date]

Summary
1. [title], [date], [time]{-[time]}
2. [title], [date], [time]{-[time]}
...
------------------------
1. [title]
[date], [time]{-[time]}, [location]
[event detail]
[poster image if available]
-------------------------
2. [title]
[date], [time]{-[time]}, [location]
[event detail]
[poster image if available]
...

"""

#TODO: p0 complete embedding photos/images/pdf, seems like doesn't support inline css style

import smtplib
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import Utils
from logging_config import *
from parse_events import parse_events


def create_human_readable_date(inp_date):
    return dt.datetime.strptime(inp_date, Utils.DATE_FORMAT).strftime(Utils.HUMAN_READABLE_DATE_FORMAT)


def create_human_readable_time(inp_time):
    return dt.datetime.strptime(inp_time, Utils.TIME_FORMAT).strftime(Utils.HUMAN_READABLE_TIME_FORMAT)


def create_human_readable_end_time(inp_time):
    if inp_time == '':
        return ''
    return ' - ' + dt.datetime.strptime(inp_time, Utils.TIME_FORMAT).strftime(Utils.HUMAN_READABLE_TIME_FORMAT)


def create_summary_item(idx, row):
    txt = str(idx) + '. ' + row['title'] + ', ' + create_human_readable_date(row['date']) + ', ' + \
          create_human_readable_time(row['start_time']) + create_human_readable_end_time(row['end_time']) + '\n'

    html = '<b>' + str(idx) + '. ' + row['title'] + ', ' + create_human_readable_date(row['date']) + ', ' + \
             create_human_readable_time(row['start_time']) + create_human_readable_end_time(row['end_time']) + \
           '</b> <br>'
    return txt, html


def create_full_item(idx, row):
    txt = '\n' + \
             str(idx) + '. ' + row['title'] + '\n' + create_human_readable_date(row['date']) + ', ' + \
          create_human_readable_time(row['start_time']) + create_human_readable_end_time(row['end_time']) + ', ' + \
          row['location'] + '\n' + row['description'] + '\n'

    html = '<hr>' + \
           '<b>' + str(idx) + '. ' + row['title'] + '<br>' + create_human_readable_date(row['date']) + ', ' + \
           create_human_readable_time(row['start_time']) + create_human_readable_end_time(row['end_time']) + ', ' + \
           row['location'] + '</b> <br>' + row['description'] + '<br>'
    if row['image']:
        html += 'Click <a href="' + row['image'] + '">here</a> to view the corresponding poster/image.<br>'
        # ext = row['image'][-4:].lower()
        # if ext == '.pdf':
        #     src_prefix = 'https://drive.google.com/viewerng/viewer?embedded=true&url='
        #     # html += '<embed src="' + src_prefix+row['image'] + '" width="300"> <br>'
        #     # html += '<embed src="' + row['image'] + '" type = "application/pdf" width="300"/> <br>'
        #     html += '[PDF cannot be loaded. Click <a href="' + src_prefix+row['image'] + '">here</a> to view.]<br>'
        #     # html += '<object width = "300" type = "application/pdf" data="' + \
        #     #         row['image'] + '" > ' + \
        #     #         '<p>[PDF cannot be loaded. Click <a href="' + row['image'] + '">here</a> to view.]</p></object>'
        # elif ext == '.png' or ext == '.jpg' or ext == '.jpeg' or ext == '.gif':
        #     html += '<img class = "inline" src="' + row['image'] + \
        #               '" alt="Poster for '+row['title'] + '" width="300"> <br>'
        # else:
        #     logging.warning('Image format not supported.')
    return txt, html


def create_email(from_email, from_pass, curr_date, duration_input, to_email):

    duration = Utils.get_duration_time_delta(duration_input)

    event_df = parse_events(curr_date, duration)

    if len(event_df) == 0:
        logging.info('No events in the specified week. NOT sending emails.')
        return

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Ashdown-Anno for ' + create_human_readable_date(curr_date)
    msg['From'] = 'Ashdown Announcements <' + from_email + '>'
    msg['To'] = to_email

    # Create the body of the message (a plain-text and an HTML version).
    txt = ''
    html = """\
    <html>
      <head>
        <style>
          html, body {
            height: 100%;
          }
          img.inline {
            height: 50 %;
            width: 50 %;
          }
        </style>
      </head>
      <body>
        <h1>Ashdown Events</h1>
        <h2>Summary</h2>
        <br>
        """

    for idx, row in event_df.iterrows():
        row_txt, row_html = create_summary_item(idx+1, row)
        txt += row_txt
        html += row_html
    for idx, row in event_df.iterrows():
        row_txt, row_html = create_full_item(idx+1, row)
        txt += row_txt
        html += row_html
    html += """\
        <!-- end main part of page -->
        </table><br/>
        <div align="center" class="smalltext" style="color:#A0A0A0;">
        &copy; 2019 MIT.
        Please report feedback about this website to ashdown-tech (at) mit.edu.<br/><br/>
        </div>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(txt, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.

    server = smtplib.SMTP('smtp.gmail.com', 587)
    # gmail SSL port: 'smtp.gmail.com:587'
    # MIT port: outgoing.mit.edu:25

    server.starttls()
    server.login(from_email, from_pass)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    logging.info("Email sent successfully!")
