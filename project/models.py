from project import db

#define db table
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    req_rate = db.Column(db.Integer, nullable=False)


    def __init__(self, req_rate):
        self.req_rate = req_rate
