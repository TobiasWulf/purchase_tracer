# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 07:18:51 2019

@author: dep17364
"""

import os
# app directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask configuration for app module.
class Config(object):
    # app cryptographic key to protect for CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''

    ADMINS = os.environ.get('ADMINS').split(',')

    # SQLAlchemy database configuration
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS'))
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Posts per page configuration
    PURCHASES_PER_PAGE = int(os.environ.get('PURCHASES_PER_PAGE'))

    # Internalization configuration
    LANGUAGES = os.environ.get('LANGUAGES').split(',')

    # Google Translator API configuration
    GOOGLE_TRANSLATOR_KEY = os.environ.get('GOOGLE_TRANSLATOR_KEY') or ''
