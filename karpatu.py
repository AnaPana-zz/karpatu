from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return "Hello Flask!"

@app.route("/rent", methods=['GET'])
def rent():
    return "Hello Flask!"

@app.route("/places", methods=['GET'])
def places():
    return "Hello Flask!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
