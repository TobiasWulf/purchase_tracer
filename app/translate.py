# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 07:18:51 2019

@author: dep17364
"""

# import json
from googletrans import Translator
# from flask_babel import _
# from app import app

translator = Translator()
translate = translator.translate
# def translate(text: str, source_language: str, dest_language: str):
#     """Translate text via Google Translation API request
#     :param text: Text to translate.
#     :type text: str.
#     :param source_language: IS639 language-identifier.
#     :type source_language: str.
#     :param dest_language: IS639 language-identifier.
#     :type dest_language: str.
#     :return: Translated text.
#     :rtype: str.
#     :raises: None
#     """
#     if 'GOOGLE_TRANSLATOR_KEY' not in app.config or not app.config['GOOGLE_TRANSLATOR_KEY']:
#         return _("Error: the translation service is not configured.")
#     else:
#         return None
