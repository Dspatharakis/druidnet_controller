import requests
import random
import time
import string
from project import db, celery, mongo_db
from project.models import Rate, FileContent 
from psycopg2 import InternalError
from celery.utils.log import get_task_logger
from PIL import Image
import os

logger = get_task_logger(__name__)

@celery.task(name="create_task_red", queue="red")
def create_task_red(img_id,start_time): # kubernetes access with nodeport and exposed port
    # print ("Image type:", img_id)
    dest_img = FileContent.objects.get(id=img_id)
    # print ("Image type:", dest_img.file)
    random_string = ''.join( random.choice(string.ascii_uppercase +string.digits) for _ in range(15))
    final_image_name = '{}'.format(random_string)
    image = Image.open(dest_img.file)
    image.save(final_image_name,'JPEG')
    try:
        result = requests.post("http://app1:6004/",files={"file": open(final_image_name,"rb")}) #"http://app1:6004/", timeout=45)
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    dest_img.delete()
    os.remove(final_image_name)
    data = Rate.query.first()
    rt = time.time() - start_time
    data.accumulative_response_time = data.accumulative_response_time + rt
    data.counter_requests = data.counter_requests + 1
    db.session.commit()
    return True

@celery.task(name="create_task_green", queue="green")
def create_task_green(img_id, start_time):
    # print ("Image type:", img_id)
    dest_img = FileContent.objects.get(id=img_id)
    print ("Image type:", dest_img.file)
    random_string = ''.join( random.choice(string.ascii_uppercase +string.digits) for _ in range(15))
    final_image_name = '{}'.format(random_string)
    image = Image.open(dest_img.file)
    image.save(final_image_name,'JPEG')
    try:
        result = requests.post("http://app2:6005/",files={"file": open(final_image_name,"rb")}) #"http://app2:6005/", timeout=45)
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    dest_img.delete()
    os.remove(final_image_name)
    data = Rate.query.first()
    art = time.time() - start_time
    data.accumulative_response_time = data.accumulative_response_time + art
    print ("art:" , art)
    data.counter_requests = data.counter_requests + 1
    db.session.commit()
    return True

@celery.task(name="create_task_queue", queue="queue")
def create_task_queue(img_id,start_time):
    print ("Image queue id:", img_id)
 
    data = Rate.query.first()
    req_rate_app1 = data.req_rate_app1 
    req_rate_app2 = data.req_rate_app2 

    from project.tasks import create_task_green,create_task_red
    propability = random.randint(0,int(req_rate_app1)+int(req_rate_app2))
    if propability < req_rate_app1:  
        task = create_task_red.delay(img_id,start_time)
    else: 
        task = create_task_green.delay(img_id,start_time)
    return True

@celery.task(queue='celery_periodic')
def update_per_interval():
    from project import celery
    client = celery.connection().channel().client
    length = client.llen('queue')
    try:
        data = Rate.query.first()
        time_passed = 1
        # if data.time_passed_since_last_event > 0: 
        if (length == 0):
            print ("queue is empty")   
            data.time_passed_since_last_event = 0 
            time_passed = 0
        req1 = float(os.environ.get("beta1", "0.5")) * data.req_rate_app1 + float(os.environ.get("alpha1", "2"))*(data.time_passed_since_last_event+time_passed)
        req2 = float(os.environ.get("beta2", "0.5")) * data.req_rate_app2 + float(os.environ.get("alpha2", "3"))*(data.time_passed_since_last_event+time_passed)
        # if req1 < 1: req1=1
        # if req2 < 1: req2=1
        data.req_rate_app1 = req1
        data.req_rate_app2 = req2
        data.time_passed_since_last_event = data.time_passed_since_last_event + time_passed 
        data.time_of_experiment = data.time_of_experiment + 1
        data.queue_size = length
        data.interval_time = data.interval_time + 1

        if (data.interval_time >= 30):
            print ("interval time is over")
            if data.counter_requests > 0:
                art = data.accumulative_response_time / data.counter_requests
                data.average_response_time = art
            else: 
                data.average_response_time = 0
            data.counter_requests = 0
            data.accumulative_response_time = 0
            data.interval_time = 0 
        db.session.commit()
        print ("Request Rate for App1: ", data.req_rate_app1, " Request Rate for App2: ",data.req_rate_app2)
        # celery.control.rate_limit('create_task_red', str(data.req_rate_app1)+"/s")
        # celery.control.rate_limit('create_task_green', str(data.req_rate_app2)+"/s")
        celery.control.rate_limit('create_task_queue', str(data.req_rate_app2 + data.req_rate_app1)+"/s")
    except InternalError:
        pass   