#!/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('api.config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

import api.models.trainer
import api.routes.routes
