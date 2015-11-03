import requests


from flask import Flask, render_template, request, flash, redirect, url_for, current_app
app = Flask(__name__)

from forms import AskQuestionForm

app.config['WTF_CSRF_SECRET_KEY'] = 'wtf_secret'
app.config['SECRET_KEY'] = 'wtf_secret'


RECAPTCHA_SECRET_KEY = '6LcWeA8TAAAAALF6fh7vfwKZsviaIaI8_bdr0Egp'

RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')


@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    form = AskQuestionForm()
    if request.method == 'POST':
        form = AskQuestionForm(request.form)
        if form.validate() and verify_recaptcha(request):
            flash("Your message was sent successfully. We'll contact you soon.")
            return redirect(url_for('contact'))
        else:
            flash_errors(form)
    return render_template('contact.html', form=form)


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


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"{error}: {field}".format(error=error, field=getattr(form, field).label.text))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
