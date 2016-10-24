'''
Email is use to send emails via the previously defined email address in the config file.
we use thread so that there is no wait for the user when he clicks on a link which enables
email sending option.
current_app gives the app name of the currently used app which has requested to send a email.
this can be neglected if we import app from app but we have to  create an app instance in
__init__ file of app.
'''


from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):     # Sending email using thread
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])      # Creating a thread
    thr.start()         #Starting a thread
    return thr
