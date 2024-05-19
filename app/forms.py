from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,TextAreaField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Donor', 'Donor'), ('Needy', 'Needy'), ('Volunteer', 'Volunteer')],
                           validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if User.load(username.data):
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if User.load(email.data):
            raise ValidationError('That email is taken. Please choose a different one.')

    def create_user(self):
        user = User(self.username.data, self.email.data, self.password.data, self.category.data)
        user.save()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def authenticate_user(self, username, password):
        user = User.load(username)
        if user and user.validate_password(password):
            return user
        return None


class CreateDonationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Canned Food', 'Canned Food'), ('Bakery', 'Bakery'), ('Produce', 'Produce')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Create Donation')