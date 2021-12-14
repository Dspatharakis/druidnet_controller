from logging import log
import os
import requests
import random
from project import app, db, celery
from project.models import Rate 
from psycopg2 import InternalError
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="create_task_red", queue="red")
def create_task_red(): # kubernetes access with nodeport and exposed port
    result =  requests.post("http://app1:6004/") #"http://app1:6004/", timeout=45)
    return True
    
@celery.task(name="create_task_green", queue="green")
def create_task_green():
    result =  requests.post("http://app2:6005/") #"http://app2:6005/", timeout=45)
    return True

@celery.task(name="create_task_queue", queue="queue")
def create_task_queue(task_type):
    data = Rate.query.first()
    req_rate_app1 = data.req_rate_app1 
    req_rate_app2 = data.req_rate_app2 

    from project.tasks import create_task_green,create_task_red
    propability = random.randint(0,req_rate_app1+req_rate_app2)
    if propability < req_rate_app1:   #1 = red
        task = create_task_red.delay()
    else:  # 2 = green
        task = create_task_green.delay()
    return True

@celery.task(queue='celery_periodic')
def update_per_interval():
    from project import celery
    client = celery.connection().channel().client
    length = client.llen('queue')
    print (length)
    time_passed = 1
    if (length == 0):
        print ("queue is empty")          
    try:
        data = Rate.query.first()
        time_passed = 1
        if (length == 0):
            print ("queue is empty")   
            data.time_passed_since_last_event = 0 
            time_passed = 0
        data.req_rate_app1 = 0.5 * data.req_rate_app1 + 1*(data.time_passed_since_last_event+time_passed)
        data.req_rate_app2 = 0.5 * data.req_rate_app2 + 2*(data.time_passed_since_last_event+time_passed)
        data.time_passed_since_last_event = data.time_passed_since_last_event + time_passed 
        db.session.commit()
        print ("Request Rate for App1: ", data.req_rate_app1, " Request Rate for App2: ",data.req_rate_app2)
        celery.control.rate_limit('create_task_red', str(data.req_rate_app1)+"/m")
        celery.control.rate_limit('create_task_green', str(data.req_rate_app2)+"/m")
        celery.control.rate_limit('create_task_queue', str(data.req_rate_app2 + data.req_rate_app1)+"/m")
    except InternalError:
        pass   