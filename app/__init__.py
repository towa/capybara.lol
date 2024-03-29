"""A small Flask app to serve daily capybara."""
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics

from app.models import User


app = Flask(__name__)

metrics = PrometheusMetrics(app)

app.config.from_object('app.config')
if not os.path.exists(app.config['CAPYBARA_PATH']):
    os.makedirs(app.config['CAPYBARA_PATH'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


from app.admin import admin
app.register_blueprint(admin, url_prefix='/admin')
from app.capybara import capybara
app.register_blueprint(capybara, url_prefix='/')
from app.api import api
app.register_blueprint(api, url_prefix='/api')