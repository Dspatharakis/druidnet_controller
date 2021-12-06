# project/main/views.py

from flask import render_template, Blueprint, jsonify, request
from object_repo import app
import time
from flask import jsonify


main_blueprint = Blueprint("main", __name__,)

@main_blueprint.route("/", methods = ['POST'])
def post():
    a = (request.get_json())
    time.sleep(1)
    resp = jsonify(success=True)
    print (resp)
    return resp


