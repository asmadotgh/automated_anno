import argparse
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging_config import *


def send_logs_email(from_email, from_pass, logs_email):
    from_email = from_email.lower()
    to_email = logs_email.lower()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Officer Recruitment logs'
    msg['From'] = 'Haosheng on behalf of AHEC <' + from_email + '>'
    msg['To'] = to_email

    msg.add_header('Content-Type', 'text')
    with open(Utils.LOGS_FILENAME) as f:
        s = f.read()
        msg.set_payload('LATEST AUTOMATED OFFICER RECRUITMENT RUN LOGS:\n\n'+s)

    # Send the message via local SMTP server.

    if from_email.endswith('@gmail.com'):

        server = smtplib.SMTP('smtp.gmail.com', 587)
        # gmail SSL port: 'smtp.gmail.com:587'
        # MIT port: outgoing.mit.edu:25
        # MIT port: outgoing.mit.edu:587, username: Kerberos username (without @mit.edu), pass: kerboras pass

        server.starttls()
        server.login(from_email, from_pass)

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

    elif from_email.endswith('@mit.edu'):
        server = smtplib.SMTP('outgoing.mit.edu:25')
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    else:
        print('Logs email not sent. Only gmail or mit email is supported for the from_email.')


def create_content(content, name):
    content = content.replace('<name>', name)
    txt = content.replace('\n', '\r\n')
    html = content.replace('\n', '\r\n <br>')
    return txt, html


def create_email(from_email, from_pass, content, to_email, to_name):
    from_email = from_email.lower()
    to_email = to_email.lower()

    content_txt, content_html = create_content(content, to_name)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Interested in becoming an Ashdown officer, {}?'.format(to_name)
    msg['From'] = 'Haosheng on behalf of AHEC <' + from_email + '>'
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
        """

    txt += content_txt
    html += content_html

    html += """\
        <!-- end main part of page -->
        <br/>
        <div align="center" class="smalltext" style="color:#A0A0A0;">
        &copy; 2019 MIT.
        Please report feedback to ashdown-anno (at) mit (dot) edu.<br/><br/>
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

    if from_email.endswith('@gmail.com'):

        server = smtplib.SMTP('smtp.gmail.com', 587)
        # gmail SSL port: 'smtp.gmail.com:587'
        # MIT port: outgoing.mit.edu:25
        # MIT port: outgoing.mit.edu:587, username: Kerberos username (without @mit.edu), pass: kerboras pass

        server.starttls()
        server.login(from_email, from_pass)

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")
    elif from_email.endswith('@mit.edu'):
        server = smtplib.SMTP('outgoing.mit.edu:25')
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")
    else:
        print('Email not sent. Only gmail or mit email is supported for the from_email.')
        logging.warning('Email not sent. Only gmail or mit email is supported for the from_email.')


# Sample usage
# python personalized_email/send_personalized_email.py --from_email=<> --from_pass=<> --content=data/content.txt --to_email_list=data/dbg.csv
if __name__ == "__main__":
    # Reset the logs file
    open(Utils.LOGS_FILENAME, 'w').close()

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--from_email', type=str,
                           default=Utils.FROM_EMAIL,
                           required=True,
                           help="<from> is an email address."
                                "The default setting uses " + Utils.FROM_EMAIL + ".")
    argparser.add_argument('--from_pass', type=str,
                           required=True,
                           help="<from_pass> password for login.")
    argparser.add_argument('--content', type=str,
                           required=True,
                           help="<content> Text file including the text.")
    argparser.add_argument('--to_email_list', type=str, required=True,
                           help="<to> is a file including names and email addresses.")
    argparser.add_argument('--logs_email', type=str, default=Utils.LOGS_EMAIL,
                           help="<bcc> is an optional email address. The log files are sent to another email to notify "
                                "Ashdown officers about success/failure of sending automated emails."
                                "If not set, the default value will be used.")
    args = argparser.parse_args()

    with open(args.content, "r") as f:
        content = f.read()

    df = pd.read_csv(args.to_email_list)

    print('\n\nThe following email will be sent: \n')
    print(content)

    print ('\n\nThe following list (#{}) will receive the email:\n'.format(len(df)))
    print (df)

    validated = ''
    while validated.lower() not in ['n', 'no', 'y', 'yes']:
        validated = input('Send email (Y/N)? ')

    if validated.lower() == 'n' or validated.lower() == 'no':
        logging.info('Email was not approved by the officer. Aborting sending email.')
    elif validated.lower() == 'y' or validated.lower() == 'yes':
        try:
            for index, row in df.iterrows():
                create_email(args.from_email, args.from_pass, content, row['email'], row['firstname'])
        finally:
            send_logs_email(args.from_email, args.from_pass, args.logs_email)
