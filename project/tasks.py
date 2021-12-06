import os
import celery
import requests
from project import app, db
from project.models import Rate 
from psycopg2 import InternalError

@celery.task(name="create_task_red", queue="red")
def create_task_red(): # kubernetes access with nodeport and exposed port
    result =  requests.post("http://app1:6004") #"http://app1:5000/", timeout=45)
    return True
    
@celery.task(name="create_task_green", queue="green")
def create_task_green():
    print (os.environ.get("APP2_IP"))
    result =  requests.post("http://app2:6005") #"http://app2:5000/", timeout=45)
    return True

@celery.task(queue='celery_periodic')
def update_per_interval():
    try:
        data = Rate.query.first()
        data.req_rate_app1 = data.req_rate_app1 + 0
        data.req_rate_app2 = data.req_rate_app2 + 0 
        print ("Request Rate for App1: ", data.req_rate_app1, " Request Rate for App2: ",data.req_rate_app2)
        db.session.commit()

        from project import celery
        celery.control.rate_limit('create_task_red', str(data.req_rate_app1)+"/m")
        celery.control.rate_limit('create_task_green', str(data.req_rate_app2)+"/m")
    except InternalError:
        pass     