import os
from flask import Flask, session, request
from config import Config
from flask_moment import Moment
import datetime

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
moment = Moment(app)