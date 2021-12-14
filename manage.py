from flask.cli import FlaskGroup
from project import app
from project.models import Rate

cli = FlaskGroup(app)

from project import db

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Rate(req_rate_app1=2,req_rate_app2=1,time_passed_since_last_event=0))
    db.session.commit()

if __name__ == "__main__":
    cli()