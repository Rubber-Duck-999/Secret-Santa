#!/usr/bin/python3
'''Python script to send '''
# Import the email modules we'll need
import smtplib
import json
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Emailer:
    '''Emailer for sending users their result'''

    def __init__(self, config):
        '''Constructor for class'''
        self.config_file   = config
        self.from_email    = ''
        self.from_password = ''

    def get_config(self):
        '''Get configuration values'''
        logging.info('# get_config()')
        try:
            if not os.path.isfile(self.config_file):
                return False
            config_file        = open(self.config_file, "r")
            config_data        = json.load(config_file)
            self.from_email    = config_data["from_email"]
            self.from_password = config_data["from_password"]
            return True
        except IOError as error:
            logging.error('File not available: {}'.format(error))
        except KeyError as error:
            logging.error('Key not available: {}'.format(error))
        except TypeError as error:
            logging.error('Type not available: {}'.format(error))
        return False

    def send(self, to_email, html):
        '''Set up message for email from stores'''
        logging.info('# send()')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            message = MIMEMultipart('alternative')
            message['Subject'] = "Secret Santa Reveal"
            message['From'] = self.from_email
            message['To'] = to_email
            message.attach(MIMEText(html, 'html'))
            logging.info('Attaching message')
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, to_email, message.as_string())
            server.close()
        except smtplib.SMTPAuthenticationError as error:
            logging.error('Error occured on auth: {}'.format(error))
        except smtplib.SMTPException as error:
            logging.error('Error occured on SMTP: {}'.format(error))
        except TypeError as error:
            logging.error('Type error on send: {}'.format(error))