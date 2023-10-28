from itertools import chain
from dotenv import load_dotenv
from email import policy
import time
import email
import imaplib
import base64
import os
import re

load_dotenv()

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')

criteria = {}
uid_max = 0

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))

mail = imaplib.IMAP4_SSL(imap_ssl_host)
mail.login(username, password)
#select the folder
mail.select('inbox')

result, data = mail.search( None, '(FROM "jgradio64")')
uids = [int(s) for s in data[0].split()]
if uids:
        # for uid in uids:
        #     # Have to check again because Gmail sometimes does not obey UID criterion.
        #     result, data = mail.fetch(str(uid), '(RFC822)')
        #     raw_email = data[0][1]
        #     email_message = email.message_from_string(raw_email)
        #     print(email_message['To'])
        #     print(email_message['Subject'])

    result, data = mail.fetch(str(uids[0]), '(RFC822.TEXT)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email, policy=email.policy.default)
    print(email_message['From'])
    print(email_message['Subject'])
    payloads = email_message.get_payload()

    for payload in payloads:
        # Check if the payload is of type text (plain text or HTML)
        if payload.get_content_type() == "text/plain" or payload.get_content_type() == "text/html":
            # Get the content of the payload as a string
            payload_text = payload.get_content()
            print(payload_text)

#Logout before running the while loop
mail.logout()