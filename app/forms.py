# -*- coding: utf-8 -*-
"""
Describe web forms for Flask. To build a User interface within the website.
So it points on the functionality part of the website where the intact with
Flask and is pushed to type in information e.g. login or registration.
The forms are described by classes. One class for each form.
Through the fact that classes are just form descriptors in usual cases there is
not init required, only public attributes for the form fields.

.. module:: forms
   :platform: Unix, Windows
   :synopsis: Describe web forms for Flask.

.. moduleauthor:: Tobias Wulf <tobias.x57756c66@gmail.com>
   :version: 0.9
   :status: development

:Classes:

    :class:`LoginForm`
    :class:`RegistrationForm`
    :class:`EditProfileForm`
    :class:`PurchaseForm`
    :class:`ResetPasswordRequestForm`
    :class:`ResetPasswordForm`

.. seealso::
    :mod:`flask_wtf`
    :mod:`wtforms`
    :mod:`wtforms.validators`
    :mod:`flask_babel`
    :mod:`app.models`

"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField,
    FloatField, DateField
)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
)
from flask_babel import lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    """Describe the user login form where the needs give his username and his
    required password. Also include a bool to remember the users credentials
    and a submit button to execute the login.

    :Class inheritance:

        FlaskForm

    :Attributes:

        :param username: Name of the user, one word.
        :type username: StringField
        :param password: Password of user, one word with special chars.
        :type password: PasswordField
        :param remember_me: Boolean if to remember user credentials or not.
                           Default False.
        :type remember_me: BooleanField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """
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
