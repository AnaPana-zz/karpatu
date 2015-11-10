from wtforms import Form, TextField, TextAreaField, validators
from wtforms.fields.html5 import EmailField

class AskQuestionForm(Form):
    name = TextField('Name', [validators.Required()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    body = TextAreaField('Message', [validators.Required()])