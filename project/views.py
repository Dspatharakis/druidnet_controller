# project/main/views.py
import os
from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request
from project import app, db
from project.models import Rate 


#from project.tasks import AddTask
main_blueprint = Blueprint("main", __name__,)



@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    from project.tasks import create_task_queue
    task = create_task_queue.delay(task_type)
    return jsonify({"task_id": task.id,"worker": task_type}), 202


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
    request_data = request.get_json()
    print (request_data)
    req_rate_app1 = request_data['req_rate_app1']
    req_rate_app2 = request_data['req_rate_app2']

    data = Rate.query.first()
    data.req_rate_app1 = req_rate_app1
    data.req_rate_app2 = req_rate_app2
    print ("Request Rate for App1: ", data.req_rate_app1, " Request Rate for App2: ",data.req_rate_app2)
    db.session.commit()
    from project import celery
    celery.control.rate_limit('create_task_red', str(data.req_rate_app1)+"/m")
    celery.control.rate_limit('create_task_green', str(data.req_rate_app2)+"/m")
    return jsonify(success=True)