from dotenv import load_dotenv
import email_retriever
import notification_sender
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



def send_notifications():
    
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    destination = os.getenv("DESTINATION_ADDRESS")
    sender = notification_sender.Notifier(smtp_username, smtp_password, smtp_host, smtp_port, destination)
    sender.send_messages(email_list)


get_yahoo_emails()
get_gmail_emails()
send_notifications()

print("Program done!")