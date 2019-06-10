"""
Describe web forms for Flask. To build a User interface within the website.
So it points on the functionality part of the website where the intact points
on purchase traces and user profile edits. The user is pushed to give
information. The forms are described by classes. One class
for each form. Through the fact that classes are just form descriptors and
inherit by FlaskForm class there is in usual cases no __init__ method required.

.. module:: forms
   :platform: Unix, Windows
   :synopsis: Describe web forms for Flask.

.. moduleauthor:: Tobias Wulf <tobias.x57756c66@gmail.com>
   :version: 1.1
   :status: development

:Classes:

    :class:`EditProfileForm`
    :class:`PurchaseForm`

.. seealso::

    :mod:`flask_wtf`
    :mod:`wtforms`
    :mod:`wtforms.validators`
    :mod:`flask_babel`
    :mod:`app.models`
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, DateField,
                     FloatField, SelectField)
from wtforms.validators import (ValidationError, DataRequired, Length,
                                NumberRange)
from flask_babel import lazy_gettext as _l
from app.models import User


# noinspection PyUnresolvedReferences
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
        :type purchaser: SelectField
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
    purchaser = SelectField(
        _l('Purchaser'),
        # choices=[],
        coerce=int,
        validators=[DataRequired()]
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
