# project/main/views.py
import base64
from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request
from project import app, db, mongo_db
from project.models import Rate, FileContent
import time
import json
from bson import json_util
from PIL import Image
import tempfile

main_blueprint = Blueprint("main", __name__,)

@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    start_time = time.time()
    file = request.files['file']
    userDoc =  FileContent().save()
    userDoc.file.put(file)
    userDoc.save()
    print ("time: ", time.time() - start_time)
    from project.tasks import create_task_queue
    id = json.loads(json_util.dumps(userDoc.id))
    img_id = str(id.get('$oid'))
    print (img_id)
    task = create_task_queue.delay(img_id)
    return jsonify({"task_id": id}), 202

@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200

@main_blueprint.route("/renew_db", methods=["POST"])
def renew_db():
    from project import celery
    client = celery.connection().channel().client
    length = client.llen('queue')
    data = Rate.query.first()
    from project import rr_app1,rr_app2,qlen,time_of_experiment
    rr_app1.set(data.req_rate_app1)
    rr_app2.set(data.req_rate_app2)
    qlen.set(length)
    temp = int(time_of_experiment) + 1
    time_of_experiment.set(temp)
    return jsonify(success=True)  # maybe intentionally make this not to work! 