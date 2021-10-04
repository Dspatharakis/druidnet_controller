from flask.cli import FlaskGroup
from project import app
from project.models import User

cli = FlaskGroup(app)

from project import db

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(User(req_rate=2))
    db.session.commit()

if __name__ == "__main__":
    cli()