from app import app, db, cli
from app.models import User, Shop, Purchase

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User, 'Shop' : Shop, 'Purchase': Purchase}