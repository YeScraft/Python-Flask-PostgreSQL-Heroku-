from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, DateTimeField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import Email, Length, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email address:", validators=[Email(), DataRequired()])
    psw = PasswordField("Password:", validators=[DataRequired(), Length(min=4, max=20)])
    remember_me = BooleanField(" Remember me: ", default=False)
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("User name:", validators=[Length(min=4, max=20), DataRequired()])
    email = StringField("Email address:", validators=[Email(), DataRequired()])
    psw = PasswordField("Password:", validators=[DataRequired(), Length(min=4, max=20)])
    psw2 = PasswordField("Password:", validators=[DataRequired(), EqualTo("psw", message="Should be equal.")])
    date = DateTimeField("Registration date")
    submit = SubmitField("Submit")


class CreateEventsForm(FlaskForm):
    author = StringField("Author name:")
    begin = DateField("It will start at:",  validators=[DataRequired()])
    end = DateField("Finish time:", validators=[DataRequired()])
    topic = StringField("Topic:", validators=[Length(min=4, max=48), DataRequired()])
    description = TextAreaField("Description:", validators=[Length(min=4, max=500), DataRequired()])
    submit = SubmitField("Submit")
