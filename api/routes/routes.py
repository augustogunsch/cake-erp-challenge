from flask import request
from sqlite3 import ProgrammingError, IntegrityError
from api.app import app, db
from api.views import trainer

@app.route('/trainer', methods=['GET'])
def route_get_trainers():
    return trainer.get_trainers()

@app.route('/trainer', methods=['POST'])
def route_create_trainer():
    return trainer.post_trainer()
