from project import db

#define db table
class Rate(db.Model):
    __tablename__ = "rates"

    id = db.Column(db.Integer, primary_key=True)
    req_rate_app1 = db.Column(db.Integer, nullable=False)
    req_rate_app2 = db.Column(db.Integer, nullable=False)


    def __init__(self, req_rate_app1,req_rate_app2):
        self.req_rate_app1 = req_rate_app1
        self.req_rate_app2 = req_rate_app2
