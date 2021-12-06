from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prometheus_flask_exporter

# instantiate the app
app = Flask(
    __name__,
)
app.config.from_object("object_repo.config.Config")
db = SQLAlchemy(app)

# register blueprints
from object_repo.views import main_blueprint
app.register_blueprint(main_blueprint)
prometheus_flask_exporter.PrometheusMetrics(app)



