from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('api.config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db)

import api.routes.routes
