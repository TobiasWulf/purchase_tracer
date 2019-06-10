from app import create_app, db, cli
from app.models import User, Shop, Purchase


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Shop=Shop, Purchase=Purchase)
