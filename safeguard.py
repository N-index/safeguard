from app import create_app, db
import os
from flask_migrate import Migrate, upgrade
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# bind db&app
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
