import requests
import random
import time
import string
from project import db, celery, mongo_db
from project.models import Rate, FileContent 
from psycopg2 import InternalError
from celery.utils.log import get_task_logger
from PIL import Image
import io 

logger = get_task_logger(__name__)

@celery.task(name="create_task_red", queue="red")
def create_task_red(img_id): # kubernetes access with nodeport and exposed port
    print ("panagitsa red:", img_id[0])
    # img_id = str(img_id.get('$oid'))
    print ("Image type:", img_id)
    start_time = time.time()
    dest_img = FileContent.objects.get(id=img_id)
    print ("Image type:", dest_img.file)
    random_string = ''.join( random.choice(string.ascii_uppercase +string.digits) for _ in range(15))
    final_image_name = '{}'.format(random_string)
    image = Image.open(dest_img.file)
    image.save(final_image_name,'JPEG')

    # f = open(final_image_name, "wb")
    # f.write(image)
    # f.close()
    print ("time: ", time.time() - start_time)
    try:
        result = requests.post("http://app1:6004/",files={"file": open(final_image_name,"rb")}) #"http://app1:6004/", timeout=45)
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    dest_img.delete()
    return True

@celery.task(name="create_task_green", queue="green")
def create_task_green(img_id):
    print ("panagitsa green:",img_id[0])
    #img_id = str(img_id.get('$oid'))
    print ("Image type:", img_id)
    start_time = time.time()
    dest_img = FileContent.objects.get(id=img_id)
    print ("Image type:", dest_img.file)
    random_string = ''.join( random.choice(string.ascii_uppercase +string.digits) for _ in range(15))
    final_image_name = '{}'.format(random_string)
    image = Image.open(dest_img.file)
    image.save(final_image_name,'JPEG')

    # f = open(final_image_name, "wb")
    # f.write(image)
    # f.close()
    print ("time: ", time.time() - start_time)
    try:
        result = requests.post("http://app2:6005/",files={"file": open(final_image_name,"rb")}) #"http://app2:6005/", timeout=45)
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    dest_img.delete()
    return True

@celery.task(name="create_task_queue", queue="queue")
def create_task_queue(img_id):
    print ("Image queue id:", img_id)
 
    data = Rate.query.first()
    req_rate_app1 = data.req_rate_app1 
    req_rate_app2 = data.req_rate_app2 

    from project.tasks import create_task_green,create_task_red
    propability = random.randint(0,req_rate_app1+req_rate_app2)
    if propability < req_rate_app1:  
        task = create_task_red.delay(img_id)
    else: 
        task = create_task_green.delay(img_id)
    return True

@celery.task(queue='celery_periodic')
def update_per_interval():
    result =  requests.post("http://web:5004/renew_db") # web:5004
    print (result)
    from project import celery
    client = celery.connection().channel().client
    length = client.llen('queue')
    time_passed = 1      
    try:
        data = Rate.query.first()
        time_passed = 1
        if (length == 0):
            print ("queue is empty")   
            data.time_passed_since_last_event = 0 
            time_passed = 0
        data.req_rate_app1 = 0.5 * data.req_rate_app1 + 2*(data.time_passed_since_last_event+time_passed)
        data.req_rate_app2 = 0.5 * data.req_rate_app2 + 3*(data.time_passed_since_last_event+time_passed)
        data.time_passed_since_last_event = data.time_passed_since_last_event + time_passed 
        db.session.commit()
        print ("Request Rate for App1: ", data.req_rate_app1, " Request Rate for App2: ",data.req_rate_app2)
        celery.control.rate_limit('create_task_red', str(data.req_rate_app1)+"/m")
        celery.control.rate_limit('create_task_green', str(data.req_rate_app2)+"/m")
        celery.control.rate_limit('create_task_queue', str(data.req_rate_app2 + data.req_rate_app1)+"/m")
    except InternalError:
        pass   