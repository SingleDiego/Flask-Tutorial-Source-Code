from flask_mail import Message
from flask import render_template, current_app
from app import mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()

    msg = Message(
        subject = '[Microblog] Reset Your Password',
        body = render_template('email/reset_password.txt', user=user, token=token),
        sender = current_app.config['MAIL_USERNAME'],
        recipients = [user.email]
    )
    mail.send(msg)

    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()