from wtforms import Form, TextField, validators

class AskQuestionForm(Form):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email Address', [validators.Required()])
    body = TextField('Message body', [validators.Required()])