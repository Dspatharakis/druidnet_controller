import time
import logging
import celery
import sqlite3
from project import app, db
from celery.app.task import Task
from project.models import User 


logger = logging.getLogger(__name__)

# import os 
# from celery import Celery


# celery = Celery(__name__)
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

class MyCoolTask(celery.Task):

    def __call__(self, *args, **kwargs):
        """In celery task this function call the run method, here you can
        set some environment variable before the run of the task"""
        logger.info("Starting to run")
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #exit point of the task whatever is the state
        logger.info("Ending run")
        pass

class AddTask(MyCoolTask):
    with app.app_context():
        try: 
            data = User.query.first()
            rate = data.req_rate
            print (rate)
        except sqlite3.OperationalError:
            print ("error")
    Task.rate_limit=''+str(rate)+'/m'

    @celery.task(name="create_task")
    def create_task(task_type):

        time.sleep(int(task_type) * 10)
        return True


@celery.task()
def update_kalman_placement():
    data = User.query.first()
    rate = data.req_rate
    data.req_rate = rate + 2  
    db.session.commit()