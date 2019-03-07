# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 11:48:43 2019

@author: dep17364
"""


from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, DateField
)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
)
from flask_babel import lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l("Repeat Password"), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_l("Please use a different email address."))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    remindings = TextAreaField(_l("Remindings"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_l("Please use a different username."))


class PurchaseForm(FlaskForm):
    purchase_date = DateField(_l('Purchase date'), format='%d.%m.%Y', validators=[DataRequired()])
    purchaser = StringField(_l('Purchaser'), validators=[DataRequired()], default='Me')
    shopname = StringField(_l('Shopname'), validators=[DataRequired()])
    value = FloatField(_l('Enter overall value of purchase'), validators=[DataRequired(), NumberRange(min=0.01)])
    subject = StringField(_l('Subject of purchase'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))
