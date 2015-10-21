from flask import Flask, render_template
app = Flask(__name__)

from forms import AskQuestionForm

@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')

@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    form = AskQuestionForm()
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
