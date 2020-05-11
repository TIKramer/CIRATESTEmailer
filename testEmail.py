#!/usr/bin/env python
# encoding: utf-8
"""
python_3_email_with_attachment.py
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.
This script works with Python 3.x
NOTE: replace values in ALL CAPS with your own values
"""

import os
import smtplib
import sys
import pymongo
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pymongo import MongoClient
import glob
import os
import slack



import json

from slack.errors import SlackApiError

from fireworks import LaunchPad

COMMASPACE = ', '
from fireworks.utilities.fw_utilities import explicit_serialize

from fireworks.core.firework import FWAction, Firework, FiretaskBase

@explicit_serialize
class Emailer(FiretaskBase):
    _fw_name = "Emailer Task"
    required_params = ["filePath"]




    def send_email(self, fw_spec):
        
        if fw_spec.__contains__('_job_info'):
            job_info_array = fw_spec['_job_info']
        else:
            job_info_array = fw_spec['_fizzled_parents']
            print(str(job_info_array))
            print(str(fw_spec))

            print(str(fw_spec['_fizzled_parents']))

            # error = "\n".join(job_info_array[-1]['launches'])

        prev_job_info = job_info_array[-1]

        sender = 'gleam.x.workflow@gmail.com'
        gmail_password = 'CIRAX2020'
        recipients = ['kramer.ian.thomas@gmail.com']

        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = "TASK: " + str(prev_job_info['name']) + " " + str(prev_job_info['state'])
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        message = ("Work flow \n\t Task ID: " + str(prev_job_info['name']) + " " + str(prev_job_info['state']))
        outer.attach(MIMEText(message))

        # List of attachments
        attachments = [
            'C:\\Users\\Cocka\\Desktop\\Thomas_Kramer_HCI_LowNHigh (1)\\Thomas_Kramer_HCI_LowNHigh\\HCI Thomas\\HiFI Report.pdf',
            str(job_info_array[0]['spec']['_job_info'][0]['launch_dir']) + '\\FW.json']

        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, gmail_password)
                s.sendmail(sender, recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise


    def run_task(self, fw_spec):




            self.send_email(fw_spec)


