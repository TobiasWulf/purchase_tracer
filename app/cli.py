from app import app
import os
import os.path as op
import glob as gl
import click


@app.cli.group()
def translate():
    """Translation and localization commands."""
    # parent command to provide base for sub commands
    # this function does not need to do anything
    pass


@translate.command()
def extract():
    """Extract the text segments which are to translate to.
    :raises: RunTimeError.
    """
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")


@translate.command()
def update():
    """Update all languages.
    :raises: RunTimeError.
    """
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel update -i messages.pot -d app/translations"):
        raise RuntimeError("update command failed")
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages.
    :raises: RunTimeError.
    """
    if os.system("pybabel compile -d app/translations"):
        raise RuntimeError("compile command failed")


@translate.command()
@click.argument('lang')
def init(lang: str):
    """Initialize a new language.
    :param lang: Language identifier after ISO639 e.g. 'de' for german or 'nl' for dutch.
    :type lang: str.
    :raises: RunTimeError.
    """
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
        raise RuntimeError("init command failed")
    os.remove('messages.pot')


@translate.command()
@click.argument('lang')
def remove(lang: str):
    """Remove language from translations.
    :param lang: Language identifier after ISO639 e.g. 'de' for german or 'nl' for dutch.
    :type lang: str.
    :raises: RunTimeError.
    """
    path = 'app/translations/' + lang
    if not op.isdir(path):
        raise RuntimeError("remove command failed")
    [os.remove(f) for f in gl.glob(op.join(path, '**'), recursive=True) if op.isfile(f)]
    [os.removedirs(d) for d in gl.glob(op.join(path, '**'), recursive=True)[::-1] if op.isdir(d)]