# -*- coding: utf-8 -*-

import requests

from collections import defaultdict
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

from forms import AskQuestionForm

import os


# constants
ADMIN_EMAIL = 'admin@it-recipes.com'
RECAPTCHA_SECRET_KEY = '6LcWeA8TAAAAALF6fh7vfwKZsviaIaI8_bdr0Egp'
RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

USER_MESSAGE_TEMPLATE = """
Приветствеум {username}!

Ваш вопрос был успешно отправлен администраторам сайта.

Мы свяжемся с Вами в ближайшее время!

Спасибо за Ваш интерес к нашему ресурсу.

{body}
"""

ADMIN_MESSAGE_TEMPLATE = """
Hi admin,

you've received a question from {username} <{email}>:

{body}"""

# flask app
app = Flask(__name__)


# mail initialization
mail = Mail()
mail.init_app(app)


# flask forms parameters
app.config['WTF_CSRF_SECRET_KEY'] = 'wtf_secret'
app.config['SECRET_KEY'] = 'wtf_secret'


# flask mail parameters
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = '2525'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME '] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD '] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER '] = ADMIN_EMAIL


@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')


@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    messages = defaultdict(list)
    form = AskQuestionForm()

    if request.method == 'POST':
        form_data = request.form
        form = AskQuestionForm(form_data)

        if form.validate() and verify_recaptcha(request):
            with mail.connect() as conn:
                user_msg = Message(
                    subject='Stara Guta: your message has been sent.',
                    body=USER_MESSAGE_TEMPLATE.format(username=form_data['name'], body=form_data['body']),
                    sender=ADMIN_EMAIL, # MAIL_DEFAULT_SENDER doesn't work for some reason
                    recipients=[form_data['email']],
                )
                admin_msg = Message(
                    subject='New question from Stara Guta website',
                    body=ADMIN_MESSAGE_TEMPLATE.format(
                        username=form_data['name'],
                        email=form_data['email'],
                        body=form_data['body']
                        ),
                    sender=ADMIN_EMAIL, # MAIL_DEFAULT_SENDER doesn't work for some reason
                    recipients=["ana7pana@gmail.com"],
                    )
                conn.send(admin_msg)
                conn.send(user_msg)
            return redirect(url_for('question_sent'))

        if not form.validate():
            for field, errors in form.errors.items():
                messages['errors'].append("{}: {}".format(','.join([e for e in errors]), field))

        if not verify_recaptcha(request):
            messages['errors'].append("Подтвердите что Вы не робот ;)")


    return render_template('contact.html', form=form, messages=messages)

@app.route("/contact/sent/", methods=['GET'])
def question_sent():
    return render_template('question_sent.html')

@app.route("/route/", methods=['GET'])
def route():
    return render_template('route.html')


@app.route("/sent/", methods=['GET', 'POST'])
def question_was_sent():
    return render_template('rent.html')


@app.route("/rent/", methods=['GET'])
def rent():
    return render_template('rent.html')


@app.route("/places/", methods=['GET'])
def places():
    return render_template('places.html')


def verify_recaptcha(request):
    data = request.form
    captcha_field_response = data.get('g-recaptcha-response')
    params = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': captcha_field_response
    }
    response = requests.get(RECAPTCHA_VERIFY_URL, params=params, verify=True)
    response = response.json()
    response["status"] = response.get("success", False)

    if response["success"]:
        return True

    return False


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
