# __author__ = "Aditi Sharma"

from django.core.mail import EmailMultiAlternatives
from WikiBreach.settings import ADMIN_EMAIL, SITE_URL
from subscription.models import SubscribedUser


def send_email(title, slug):
    list = SubscribedUser.get_emails()
    for email in list:
        print("Sending email to: " + email)
        content = SITE_URL + "/posts/"+slug
        subject, from_email, to = 'WikiBreach Alert', ADMIN_EMAIL, email
        text_content = "New breach has been reported"
        html_content = '<strong>A new breach has been reported </strong><a href='+'\"'+ content +'\"'+'target=\"_blank\"><h1>' + title + '</h1></a><br> <p> Visit wikibreach today to view all the details </p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


