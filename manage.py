from flask.cli import FlaskGroup
from project import app
from project.models import Rate

cli = FlaskGroup(app)

from project import db, mongo_db

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Rate(req_rate_app1=2,req_rate_app2=1,time_passed_since_last_event=0,time_of_experiment = 0,queue_size=0,average_response_time=0,accumulative_response_time=0,counter_requests=0,interval_time=0))
    db.session.commit()

if __name__ == "__main__":
    cli()