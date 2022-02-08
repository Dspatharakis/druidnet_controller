from project import db,mongo_db
from bson.objectid import ObjectId


#define db table
class Rate(db.Model):
    __tablename__ = "rates"

    id = db.Column(db.Integer, primary_key=True)
    req_rate_app1 = db.Column(db.Float, nullable=False)
    req_rate_app2 = db.Column(db.Float, nullable=False)
    time_passed_since_last_event = db.Column(db.Float, nullable=False)
    time_of_experiment = db.Column(db.Float, nullable=False)
    queue_size = db.Column(db.Float, nullable=False)
    average_response_time = db.Column(db.Float, nullable=False)
    accumulative_response_time = db.Column(db.Float, nullable=False)
    counter_requests = db.Column(db.Float, nullable=False)
    interval_time = db.Column(db.Float, nullable=False)
    def __init__(self, req_rate_app1,req_rate_app2,time_passed_since_last_event,time_of_experiment,queue_size,average_response_time,accumulative_response_time, counter_requests,interval_time):
        self.req_rate_app1 = req_rate_app1
        self.req_rate_app2 = req_rate_app2
        self.time_passed_since_last_event = time_passed_since_last_event
        self.time_of_experiment  = time_of_experiment 
        self.queue_size = queue_size
        self.average_response_time = average_response_time
        self.accumulative_response_time = accumulative_response_time
        self.counter_requests = counter_requests
        self.interval_time = interval_time
# Picture table. By default the table name is filecontent
class FileContent(mongo_db.Document):

    """ 
    The first time the app runs you need to create the table. In Python
    terminal import db, Then run db.create_all()
    """
    """ ___tablename__ = 'yourchoice' """ # You can override the default table name

    id = mongo_db.ObjectIdField(default=ObjectId, primary_key=True)
    file = mongo_db.ImageField()
    # def __repr__(self):
    #     return f'Pic Name: {self.name} Data: {self.data}'

