from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class ContactUs(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('First Name',
                        validators=[DataRequired(), Email(), Length(min=2, max=255)])
    subject = StringField('Last Name',
                          validators=[DataRequired(), Length(min=2, max=255)])
    message = TextAreaField('Mobile Number',
                            validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Send')
