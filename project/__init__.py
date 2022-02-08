import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import celery_config
import prometheus_flask_exporter
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from flask_mongoengine import MongoEngine


# instantiate the app
app = Flask(
    __name__,
    template_folder="./client/templates",
    static_folder="./client/static",
)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
mongo_db = MongoEngine(app)

# register blueprints
metrics = GunicornPrometheusMetrics(app)
metrics = prometheus_flask_exporter.PrometheusMetrics(app)
from project.views import main_blueprint
app.register_blueprint(main_blueprint)

def make_celery(app):
    celery = Celery(
        app.import_name,
    )
    celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    celery.conf.update(app.config)
    celery.conf.update(
    task_annotations={
        # 'create_task_green': {
        #     'rate_limit': '1/s'  # Default is 1 per minute
        # },
        #  'create_task_red': {
        #     'rate_limit': '2/s'  # Default is 2 per minute
        # },
          'create_task_queue': {
            'rate_limit': '1/s'  # Default is 3 per minute
        }
    },
    )

    celery.config_from_object(celery_config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
celery = make_celery(app)