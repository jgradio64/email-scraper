from dotenv import load_dotenv
import email_retriever
import os

load_dotenv()
# Initialize list as empty
email_list = []

def get_yahoo_emails():
    imap_ssl_host = os.getenv('YAHOO_IMAP_HOST')
    imap_username = os.getenv('YAHOO_EMAIL_ADDRESS')
    imap_password = os.getenv('YAHOO_PASSWORD')

    retriever = email_retriever.EmailRetriever(imap_username, imap_password, imap_ssl_host, 5)
    retriever.run()
    email_list.extend(retriever.get_email_list())


def get_gmail_emails():
    imap_ssl_host = os.getenv('GMAIL_IMAP_HOST')
    imap_username = os.getenv('GMAIL_EMAIL_ADDRESS')
    imap_password = os.getenv('GMAIL_PASSWORD')

    retriever = email_retriever.EmailRetriever(imap_username, imap_password, imap_ssl_host, 5)
    retriever.run()
    email_list.extend(retriever.get_email_list())


get_yahoo_emails()
get_gmail_emails()

print("Program done!")