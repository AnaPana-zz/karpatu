from wtforms import Form, TextField, TextAreaField, validators

class AskQuestionForm(Form):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Required()])
    body = TextAreaField('Message', [validators.Required()])