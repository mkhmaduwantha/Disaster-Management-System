import os
import secrets
from PIL import Image
from flask import url_for, current_app, render_template
from flask_login import current_user
from flask_mail import Message
from emas import mail
from itsdangerous import URLSafeTimedSerializer


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext


<< << << < HEAD
picture_path = os.path.join(
    current_app.root_path, 'static/profile_pics', picture_fn)

output_size = (125, 125)
== == == =
picture_path = os.path.join(current_app.root_path,
                            'static/profile_pics', picture_fn)

output_size = (125, 125)
>>>>>> > c637c275386d1a45104676601bfb14f10ecd9688
i = Image.open(form_picture)
i.thumbnail(output_size)
i.save(picture_path)

return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='shawnmars9390@gmail.com', recipients=[user.email])
    link = url_for('users.reset_token', token=token, _external=True)
    msg.body = f'''To reset your password visit the following link:
    
    If you did not make this request then ignore this email and no change will happen.
    '''
    msg.html = render_template(
        '/user/reset_email.html',  link=link)

    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_reset_token()
    msg = Message('Email Confirmation',
                  sender='shawnmars9390@gmail.com', recipients=[user.email])
    link = url_for('users.confirm_email', token=token, _external=True)

    msg.body = f'''To confirm your email visit the following link:
    

    If you did not make this request then ignore this email and no change will happen.
    '''
    msg.html = render_template(
        '/user/reset_email.html',  link=link)
    mail.send(msg)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
