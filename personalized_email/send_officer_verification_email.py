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
    msg['Subject'] = 'Officer Verification logs - Fall 2020'
    msg['From'] = 'Haosheng on behalf of AHEC <' + from_email + '>'
    msg['To'] = to_email

    msg.add_header('Content-Type', 'text')
    with open(Utils.LOGS_FILENAME) as f:
        s = f.read()
        msg.set_payload('LATEST AUTOMATED OFFICER VERIFICATION RUN LOGS:\n\n'+s)

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


def create_content(from_email, content, to_email, reply_to_email, from_term, to_term):
    from_email = from_email.lower()
    to_email = to_email.lower()

    content = content.replace('<from_term>', from_term)
    content = content.replace('<to_term>', to_term)
    content_txt = content.replace('\n', '\r\n')
    content_html = content.replace('\n', '\r\n <br>')

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Confirming your Ashdown officer status'
    msg['From'] = 'Haosheng on behalf of AHEC <' + from_email + '>'
    msg['To'] = to_email
    msg.add_header('reply-to', reply_to_email)

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
            &copy; 2020 MIT.
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

    return msg


def send_emails(from_email, from_pass, reply_to_email, content, df):
    from_email = from_email.lower()
    reply_to_email = reply_to_email.lower()

    # Send the message via local SMTP server.

    if from_email.endswith('@gmail.com'):

        server = smtplib.SMTP('smtp.gmail.com', 587)
        # gmail SSL port: 'smtp.gmail.com:587'
        # MIT port: outgoing.mit.edu:25
        # MIT port: outgoing.mit.edu:587, username: Kerberos username (without @mit.edu), pass: kerboras pass

        server.starttls()
        server.login(from_email, from_pass)

    elif from_email.endswith('@mit.edu'):
        server = smtplib.SMTP('outgoing.mit.edu:25')

    else:
        print('Email not sent. Only gmail or mit email is supported for the from_email.')
        logging.warning('Email not sent. Only gmail or mit email is supported for the from_email.')

    for index, row in df.iterrows():
        try:
            if '@' in str(row['Email']):
                to_email = row['Email']
                msg = create_content(from_email, content, to_email, reply_to_email, row['First_Term'], row['Last_Term'])
                server.sendmail(from_email, to_email, msg.as_string())
                logging.info("Email sent successfully to {}!".format(to_email))
        except:
            logging.warning('Exception occurred. Email was not sent to {}.'.format(to_email))

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.quit()


# Sample usage
# python personalized_email/send_officer_verification_email.py --from_email=<> --from_pass=<> --reply_to_email=<> --content=data/officer_verification_content.txt --to_email_list=data/dbg_officers.csv --logs_email=asma_gh@mit.edu
# officer_list_fall_2020.txt
if __name__ == "__main__":
    # Reset the logs file
    open(Utils.LOGS_FILENAME, 'w').close()

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--from_email', type=str,
                           default=Utils.FROM_EMAIL,
                           required=True,
                           help="<from> is an email address."
                                "The default setting uses " + Utils.FROM_EMAIL + ".")
    argparser.add_argument('--reply_to_email', type=str,
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

    print('\n\nThe following list (#{}) will receive the email:\n'.format(len(df)))
    print(df)

    print('From email: {}'.format(args.from_email))
    print('Reply to email: {}'.format(args.reply_to_email))
    print('Logs email: {}'.format(args.logs_email))

    validated = ''
    while validated.lower() not in ['n', 'no', 'y', 'yes']:
        validated = input('Send email (Y/N)? ')

    if validated.lower() == 'n' or validated.lower() == 'no':
        logging.info('Email was not approved by the officer. Aborting sending email.')
    elif validated.lower() == 'y' or validated.lower() == 'yes':
        try:
            send_emails(args.from_email, args.from_pass, args.reply_to_email, content, df)
        finally:
            send_logs_email(args.from_email, args.from_pass, args.logs_email)
