from django.core.mail import send_mail, EmailMessage
from django.conf import settings

import threading

def send_invitation_email(sender_email,subject, message, receiver_email):
    send_mail(subject, message, sender_email, [receiver_email], fail_silently=False)

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]
        )
        EmailThread(email).start()