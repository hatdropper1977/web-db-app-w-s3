from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, IPAddress

# Form ORM
class QuizForm(FlaskForm):
        agree = BooleanField('Check this box if you would like')
	anumber = IntegerField('Enter a number',validators = [InputRequired()])
	ipaddr = StringField('Enter an IP address', validators=[IPAddress()])
	textblob =  TextAreaField('Who do you think won the console wars of 1991, Sega Genesis or Super Nintendo? (2048 characters)', validators=[InputRequired(),Length(max=2047)] )
        submit = SubmitField('Submit')
