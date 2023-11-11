from itertools import chain
from dotenv import load_dotenv
from email import policy
from email.header import decode_header
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
    '''
    Purpose: Builds a date string for the mail search function
    Input: An integer that indicates how far back you want to check
    Output: A string in the format 'day-month-year', uses textual shorthand for month.
    Output example: "01-Jan-1990"
    '''
    today = datetime.datetime.now()
    target_date = today - datetime.timedelta(days = days_ago)
    day = target_date.day
    month = target_date.strftime('%b')
    year = target_date.year
    date_string = str(day) + "-" + month + "-" + str(year)
    return date_string


def helper_decode(encoded_array):
    result = encoded_array
    # Decode any byte strings.
    for x in range(len(result)):
        if isinstance(result[x], bytes):
            result[x] = result[x].decode('utf-8')
        elif isinstance(x, str):
            pass
    return result


def flatten(array):
    return [e for l in array for e in l]


def helper_filter(array):
    result = array
    if "utf-8" in result:
        result.remove("utf-8")
    if None in result:
        result.remove(None)
    return result


def retrieve_single_email(uid):
    result, data = mail.fetch(str(uid), '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    sender = decode_header(email_message['From'])
    subject = decode_header(email_message['Subject'])
    # Flatten the list of tuples into just a list
    # Then get just the part that has the email address
    sender = flatten(sender)
    subject = flatten(subject)

    sender = helper_decode(sender)
    subject = helper_decode(subject)

    sender = helper_filter(sender)
    subject = helper_filter(subject)

    print(sender)
    print(subject)


def search_emails(email_name):
    search_string = '(FROM "'+ email_name +'" SENTSINCE ' + build_date(11) + ')'

    result, data = mail.search( None, search_string)
    uids = [int(s) for s in data[0].split()]
    if uids:
        for uid in uids:
            retrieve_single_email(uid)
            

load_dotenv()

imap_ssl_host = os.getenv('GMAIL_SSL_HOST')
imap_ssl_port = 993
username = os.getenv('GMAIL_EMAIL_ADDRESS')
password = os.getenv('GMAIL_PASSWORD')

uid_max = 0

mail = imaplib.IMAP4_SSL(imap_ssl_host)
mail.login(username, password)
#select the folder
mail.select('inbox')

search_emails("citi")

#Logout of the mail server
mail.logout()

