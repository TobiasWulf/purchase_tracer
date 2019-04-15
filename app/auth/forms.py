"""
Describe authentications web forms for Flask. To build a login, sign up and
password reset user interface within the website. So it points on the
functionality part of the website where the user intact with Flask and is
pushed to type in information. The forms are described by classes. One class
for each form. Through the fact that classes are just form descriptors and
inherit by FlaskForm class there is in usual cases no __init__ method required.

.. module:: auth.forms
   :platform: Unix, Windows
   :synopsis: Describe web forms for Flask.

.. moduleauthor:: Tobias Wulf <tobias.x57756c66@gmail.com>
   :version: 1.1
   :status: development

:Classes:

    :class:`LoginForm`
    :class:`RegistrationForm`
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
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
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

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l("Please use a different email address."))

    def validate_username(self, username):
        """Validate username if it is already in the user table of the
        database. If it is in the database a validation error will be raised.

        :Errors:

            :raises: ValidationError
        """

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l("Please use a different username."))


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
    submit = SubmitField(_l("Request Password Reset"))


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
