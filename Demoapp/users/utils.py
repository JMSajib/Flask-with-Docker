import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from Demoapp import app, mail


def save_picture(form_picture):
    randorm_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randorm_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_rest_token()
    msg = Message('Password Reset Request',sender='jm.sajib012@gmail.com',
                    recipients=[user.email])
    msg.body = f'''To Reset your Password, visit the following Link:
        {url_for('users.reset_token',token=token,_external=True)}
        This Following Link will be Expired Within 30 minutes.
    '''
    mail.send(msg)
