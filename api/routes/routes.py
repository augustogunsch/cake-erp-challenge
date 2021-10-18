from flask import request
from sqlite3 import ProgrammingError, IntegrityError
from api.app import app, db
from api.views import trainer

@app.route('/trainer/<int:trainerId>', methods=['GET'])
def route_get_trainer(trainerId):
    return trainer.get_trainer(trainerId)

@app.route('/trainer', methods=['GET'])
def route_get_trainers():
    return trainer.get_trainers()

@app.route('/trainer', methods=['POST'])
def route_create_trainer():
    return trainer.post_trainer()

@app.route("/trainer/authenticate", methods=['POST'])
def route_auth_trainer():
    return trainer.auth_trainer()
