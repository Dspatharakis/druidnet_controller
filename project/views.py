# project/main/views.py

from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request
from project import app, db
from project.models import User 
#from project.tasks import AddTask

main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET"])
def home():
    data = User.query.first()# db.session.query(User).first() 
    print (data)
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    from project.tasks import AddTask
    task = AddTask.create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200