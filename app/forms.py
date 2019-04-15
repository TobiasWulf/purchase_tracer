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
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField,
    FloatField, DateField
)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
)
from flask_babel import lazy_gettext as _l
from app.models import User





