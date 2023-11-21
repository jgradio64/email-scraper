from itertools import chain
from dotenv import load_dotenv
from email import policy
from email.header import decode_header
import datetime
import email
import imaplib
import json
import os
        

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


def extract_email_address(sender_array):
    res = [i.find('@') for i in sender_array]
    for x in range(len(res)):
        if(res[x] > 0):
            return sender_array[x]
    


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

    sender_address = extract_email_address(sender)
    subject = subject[0]

    print("From: " + sender_address)
    print("\t" + subject)


def search_emails(email_name):
    search_string = '(FROM "'+ email_name +'" SENTSINCE ' + build_date(4) + ')'

    result, data = mail.search( None, search_string)
    uids = [int(s) for s in data[0].split()]
    if uids:
        for uid in uids:
            retrieve_single_email(uid)
            

def check_senders():
    f = open("senders.json")
    senders = json.load(f)
    for sender in senders:
        search_emails(sender)


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

check_senders()

#Logout of the mail server
mail.logout()
