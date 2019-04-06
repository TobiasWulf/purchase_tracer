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


# noinspection PyUnresolvedReferences
class LoginForm(FlaskForm):
    """Describe the user login form. The user needs to give his username and
    required password. Also include a bool to remember the users credentials
    and a submit button to execute the login.

    :Class Inheritance:

        FlaskForm

    :Attributes:

        :param username: Name of the user, one word. It is input required to
                         validate the field on submit.
        :type username: StringField
        :param password: Password of user, one word with special chars. It is
                         input required to validate the field on submit.
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


# noinspection PyUnresolvedReferences
class RegistrationForm(FlaskForm):
    """Registration form is similar equal to the LoginForm class.
    Differences are the second password field and a functionality to validate
    the email if it is already existing in the database.

    :Class Inheritance:

        FlaskForm

    :Attributes:

        :param username: Name of the user, one word. It is input required to
                         validate the field on submit.
        :type username: StringField
        :param email: User email. Standard email address. Input and standard
                      email validation.
        :param password: Password of user, one word with special chars. It is
                         input required to validate the field on submit.
        :type password: PasswordField
        :param password2: Password of user, one word with special chars. It is
                         input required and needs to be equal to passwordto
                         validate the field on submit.
        :type password2: PasswordField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """

    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l("Repeat Password"), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        """Validate email address if it is already in the user table of the
        database. If it is in the database a validation error will be raised.

        :Errors:

            :raises: ValidationError
        """

        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_l("Please use a different email address."))


class EditProfileForm(FlaskForm):
    """Edit user profile form describes the user interface for editable user
    data. This includes a text field for user entered information.

    :Class Inheritance:

        FlaskForm

    :Attributes:

        :param username: Name of the user, one word. It is input required to
                         validate the field on submit. The username is fetched
                         from current user and validated with the app database
                         and just displayed.
        :type username: StringField
        :param remindings: Text field for entering additional user information
        :type remindings: TextAreaField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """

    username = StringField(_l('Username'), validators=[DataRequired()])
    remindings = TextAreaField(
        _l("Remindings"),
        validators=[Length(min=0, max=140)]
    )
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        """Class super initialization to get current user name and validate
        later with original site user name."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Validate current username which is visiting the with oirganl
        username of the user page. Raise error if it is tried to make changes
        to a user profile which is not assigned to the current user.

        :Attributes:

            :param username: Username of current user page.
            :type username: str

        :Errors:

            :raises: ValidationError
        """

        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_l("Please use a different username."))


# noinspection PyUnresolvedReferences
class PurchaseForm(FlaskForm):
    """Describe the form to log the single purchases.

    :Class Inheritance:

        FlaskForm

    :Attributes:

        :param purchase_date: Date of purchase of date format DD-MM-YYYY.
        :type purchase_date: DateField
        :param purchaser: User who did the purchase.
        :type purchaser: StringField
        :param shopname: Shop where the purchase was done.
        :type shopname: StringField
        :param subject: Main theme of the purchase.
        :type subject: StringField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """

    purchase_date = DateField(
        _l('Purchase date'),
        format='%d.%m.%Y',
        validators=[DataRequired()]
    )
    purchaser = StringField(
        _l('Purchaser'),
        validators=[DataRequired()],
        default='Me'
    )
    shopname = StringField(_l('Shopname'), validators=[DataRequired()])
    value = FloatField(
        _l('Enter overall value of purchase'),
        validators=[DataRequired(), NumberRange(min=0.01)]
    )
    subject = StringField(
        _l('Subject of purchase'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Submit'))


# noinspection PyUnresolvedReferences
class ResetPasswordRequestForm(FlaskForm):
    """Describes the user dialog for the case that the user forgot his
    password. The user has to enter his email address and on submit the
    password reset flow is started.

    :Attributes:

        :param email: User email. Needs to entered by user.
        :type email: StringField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """

    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Reset'))


class ResetPasswordForm(FlaskForm):
    """As follow of the password reset request this form gets user to the
    password reset interface. The principle is equal to the sign in form.

    :Attributes:

        :type password: PasswordField
        :param password2: Password of user, one word with special chars. It is
                         input required and needs to be equal to passwordto
                         validate the field on submit.
        :type password2: PasswordField
        :param submit: Submit button to execute the action.
        :type submit: SubmitField
    """

    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'),
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Reset Password'))
