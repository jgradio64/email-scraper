import smtplib, ssl

class Notifier:
    def __init__(self, username, password, host, port, destination):
        self.username = username
        self.password = password
        self.host = host
        self.dest = destination
        self.port = port


    def send_messages(self, msg_ary):

        context = ssl.create_default_context()

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls(context=context)
            server.login(self.username, self.password)
            for msg in msg_ary:
                # Tried doing the string formatting as a seperate function, but it just workes easiest/cleanest this way. IDK
                fmt = '{}\r\n\r\nSubject: {}'
                sender = msg["sender"]
                subject = msg["subject"]
                server.sendmail(self.username, self.dest, fmt.format(sender, subject).encode('utf-8'))
        except Exception as e:
            # Print any error messages to terminal
            print(e)
        finally:
            server.quit() 


