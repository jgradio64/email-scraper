from itertools import chain
from dotenv import load_dotenv
from email import policy
import datetime
import time
import email
import imaplib
import base64
import os
import re


def process_payloads(payload):
    if isinstance(payload, list):
        for sub_payload in payload:
            process_payloads(sub_payload)
    elif isinstance(payload, list):
        for sub_payload in payload:
            process_payloads(sub_payload)
    elif isinstance(payload, str):
        # Handle the text content
        return payload
    else:
        content_type = payload.get_content_type()
        if content_type == "text/plain":
            payload_text = payload.get_content()
            return payload_text
        

def build_date(days_ago):
    today = datetime.datetime.now()
    target_date = today - datetime.timedelta(days = days_ago)
    day = target_date.day
    month = target_date.strftime('%b')
    year = target_date.year
    date_string = str(day) + "-" + month + "-" + str(year)
    return date_string


def decode_subject(encoded_subject):
    # Split the string into parts and decode each part
    decoded_parts = email.header.decode_header(encoded_subject)

    # Reconstruct and decode the string
    decoded_string = ''
    for part, charset in decoded_parts:
        if charset is not None:
            decoded_string += part
        else:
            # If charset is None, assume UTF-8
            decoded_string += part

    return decoded_string


def search_emails(email_name):
    search_string = '(FROM "'+ email_name +'" SENTSINCE ' + build_date(11) + ')'

    result, data = mail.search( None, search_string)
    uids = [int(s) for s in data[0].split()]
    if uids:
        for uid in uids:
            result, data = mail.fetch(str(uids[0]), '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            sender = email_message['From']
            subject = decode_subject(email_message['Subject'])

            # 
            if ("statement" in subject):
                result, data = mail.fetch(str(uids[0]), '(RFC822.TEXT)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email, policy=email.policy.default)
                body = process_payloads(email_message.get_payload())
                body = decode_subject(body)
                print("FROM: " + sender + "\nSUBJECT: " + subject + "\nBODY:\n" + "You have a new statement.")
            else:
                print("FROM: " + sender + "\nSUBJECT: " + subject)

load_dotenv()

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')

uid_max = 0

mail = imaplib.IMAP4_SSL(imap_ssl_host)
mail.login(username, password)
#select the folder
mail.select('inbox')

search_emails("citi")

#Logout before running the while loop
mail.logout()

