***************
Purchase Tracer
***************

* Application status: devolopement

Intention
#########

Track all purchases of flat mates and analyze the amount and overal price if they are in balance.

Source
======

This is a Python Flask application based on this awesome `tutorial <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars>`_ by `Miguel Grinberg <https://plus.google.com/u/0/+MiguelGrinberg>`_.

Additions
=========

In addition to that blog feature (tutorila) the application includes a table view of datasets and some dynamic plots to visualize
the purchase data.

Current Chapter (tutorial)
##########################

* Chapter 15: `Better Application Structure <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure>`_

Flask application handling and deployment
#########################################

Commands and hints to handle this application from shell or console (linux).

.. note::
   * All commands must be entered in toplevel of directory ~/purchase_tracer in a activated virtual environment prompt.

Application handling
====================

Commands to initialize the Flask from shell. This contains database initialization, support content translation (client site),
run a mail server in devolopement mode for debugging, run app by shell and python interpreter in a flask shell.

Init app
--------

* Run following commands in environment prompt (fist time):

    >>> flask db init

    * run this only when you made new models to app.db in app/models.py

    >>> flask db migrate -m "<your changes at db>"
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.autogenerate.compare] Detected added column "<your changes at db>"
    Generating ~/purchase_tracer/migrations/versions/6343d61b0d50_<your_changes_at_db>.py ... done

    * run this after init or migrate

    >>> flask db upgrade
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade ea8b9621c899 -> 6343d61b0d50, <your changes at db>


Start app
---------

* Environment prompt:

    >>> flask run

* then open browser and enter "localhost:8000"

Flask environment shell
-----------------------

* Flask environment variables are set in the .flaskenv file
* shell context is defined in purchase_tracer.py
* to run a python shell with flask environment of the app enter in anaconda prompt:

    >>> flask shell

Python Email Server (debugging)
-------------------------------

* Run this from environment console:

    >>> python -m smtpd -n -c DebuggingServer localhost:8025

Extracting Text to Translate (Flask-Babel)
------------------------------------------

* Run commands in environment console

    >>> pybabel extract -F babel.cfg -k _l -o messages.pot .

    * german: de, dutch: nl, thai: th, etc. ISO639

    >>> pybabel init -i messages.pot -d app/translations -l de
    >>> pybabel compile -d app/translations
    >>> pybabel update -i messages.pot -d app/translations (update translation)

* add command-line enhancements to flask (coded in purchase_tracer.py and app/cli.py)

    * execute in top-directory and activate environment prompt

        * for help run

        >>> flask translate --help

        * to extract the text which is to translate to

        >>> flask translate extract

        * to initialize the language support in a specific language such as de, en, nl, etc.

        >>> flask translate init <ISO639 language-identifier>

        * after fill out translations segments in a messages.po file run update

        >>> flask translate update

        * compile in to Flask framework

        >>> flask translate compile

        * remove language support

        >>> flask translate remove <ISO639 language-identifier>


Requirements
############

Requirements for virtual python environment.

Found Requirements in Conda Cloud
=================================

* Run this in Anaconda Prompt:

    >>> conda install -c anaconda flask mysqlclient sqlalchemy flask-sqlalchemy werkzeug flask-login wtforms pyjwt click
    >>> conda install -c conda-forge python-dotenv flask-wtf flask-migrate flask-mail flask-bootstrap flask-moment flask-babel requests
    >>> pip install guess_language-spirit googletrans
