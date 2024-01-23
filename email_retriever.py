from email.header import decode_header
import helper_functions as hf
import email
import imaplib
import json


class EmailRetriever:
    def __init__(self, username, password, host, days_ago):
        self.username = username
        self.password = password
        self.host = host
        self.days_ago = days_ago
        self.retrieved_emails = []


    def retrieve_single_email(self, uid):
        result, data = self.mail.fetch(str(uid), '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        sender = decode_header(email_message['From'])
        subject = decode_header(email_message['Subject'])

        sender = hf.flatten(sender)
        subject = hf.flatten(subject)

        sender = hf.helper_decode(sender)
        subject = hf.helper_decode(subject)

        sender = hf.helper_filter(sender)
        subject = hf.helper_filter(subject)

        sender_address = hf.extract_email_address(sender)
        subject = subject[0]

        self.retrieved_emails.append({"sender":sender_address,"subject":subject})


    def search_emails(self, email_name):
        search_string = '(FROM "' + email_name + '" SENTSINCE ' + hf.build_date(self.days_ago) + ')'

        result, data = self.mail.search(None, search_string)
        uids = [int(s) for s in data[0].split()]
        if uids:
            for uid in uids:
                self.retrieve_single_email(uid)


    def check_senders(self):
        f = open("senders.json")
        senders = json.load(f)
        for sender in senders:
            self.search_emails(sender)


    def run(self):
        self.mail = imaplib.IMAP4_SSL(self.host)
        self.mail.login(self.username, self.password)
        # select the folder
        self.mail.select('inbox')

        self.check_senders()

        # Logout of the mail server
        self.mail.logout()


    def get_email_list(self):
        return self.retrieved_emails
