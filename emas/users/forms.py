from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from emas.models import User

class RegistrationForm(FlaskForm):
    title = StringField('Title',
                           validators=[DataRequired(), Length(min=2, max=20)])
    fname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=255)])
    lname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=255)])
    mobile_number = StringField('Mobile Number',
                           validators=[DataRequired(), Length(min=2, max=20)])
    user_type = SelectField(
        u'User Type',
        choices = [('None', 'none'), ('Military', 'military'),('Camp', 'camp')]
    )
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_fname(self,fname):
        user = User.query.filter_by(fname=fname.data).first()

        if user:
            raise ValidationError('That fname is taken please choose a different one.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    title = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    fname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    mobile_number = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()],render_kw={'readonly': True})
    user_type = StringField('User Type',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={'readonly': True})

    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')


    def validate_fname(self,fname):
        if fname.data != current_user.fname:
            user = User.query.filter_by(fname=fname.data).first()

            if user:
                raise ValidationError('That fname is taken please choose a different one.')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('That email is taken please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('request Passworrd Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')

class UpdateAccountFormUser(FlaskForm):

        home_number = StringField('Home Telephone', validators=[DataRequired()])
        line_one = StringField('Address line one', validators=[DataRequired()])
        line_two = StringField('Address line two', validators=[DataRequired()])
        province = StringField('Province', validators=[DataRequired()]) 
        district = StringField('District', validators=[DataRequired()])
        city = StringField('City', validators=[DataRequired()])
        postal_code = StringField('Postal Code', validators=[DataRequired()])

        
        submit = SubmitField('Update')

class UpdateAccountFormMilitary(FlaskForm):
        designation = StringField('Designation', validators=[DataRequired()])
        office_number = StringField('Office Telephone', validators=[DataRequired()])
        line_one = StringField('Address line one', validators=[DataRequired()])
        line_two = StringField('Address line two', validators=[DataRequired()])
        province = StringField('Province', validators=[DataRequired()])
        district = StringField('District', validators=[DataRequired()])
        city = StringField('City', validators=[DataRequired()])
        postal_code = StringField('Postal Code', validators=[DataRequired()])

        
        submit = SubmitField('Update')

class UpdateAccountFormCamp(FlaskForm):

        camp_name = StringField('Camp Name', validators=[DataRequired()])
        camp_number = StringField('Camp Telephone', validators=[DataRequired()])
        line_one = StringField('Address line one', validators=[DataRequired()])
        line_two = StringField('Address line two', validators=[DataRequired()])
        province = StringField('Province', validators=[DataRequired()])
        district = StringField('District', validators=[DataRequired()])
        city = StringField('City', validators=[DataRequired()])
        postal_code = StringField('Postal Code', validators=[DataRequired()])
        remaining_beds = StringField('Remaining Beds',render_kw={'readonly': True})
        total_beds = StringField('Total Beds', validators=[DataRequired()])
        occupied_beds = StringField('Occupied Beds', validators=[DataRequired()])
        camp_needs = TextAreaField('Needs', validators=[DataRequired()])
        
        submit = SubmitField('Update')