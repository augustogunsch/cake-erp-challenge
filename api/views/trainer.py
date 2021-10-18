from sqlalchemy.exc import NoResultFound, IntegrityError
from api.models.trainer import Trainer, trainer_schema, trainer_schemas, InvalidTeam
from api.app import db
from api.app import app
from flask import request, jsonify
from .errors import ParsingError, ConflictingParameters, ConflictingResources, AuthenticationFailure
from werkzeug.security import check_password_hash
import datetime
import jwt

def get_trainer(id):
    try:
        return trainer_schema.dump(Trainer.query.get(id))
    except:
        return jsonify({})

def get_trainers():
    args = request.args

    try:
        limit = int(args.get("limit", -1))
        offset = int(args.get("offset", 0))
    except ValueError:
        return ParsingError("Couldn't parse parameter as integer")

    if limit < -1 or offset < 0:
        return ParsingError("Expected positive integer as parameter")

    nickname = args.get("nickname", "")
    nickname_contains = args.get("nickname_contains", "")

    try:
        if nickname:
            if nickname_contains:
                return ConflictingParameters("nickname and nickname_contains are mutually exclusive")

            query = Trainer.query.filter_by(nickname=nickname).limit(limit).offset(offset)
            return trainer_schemas.dumps(query.all())

        else:               # se nickname_contains também está vazio, retornará todos trainers
            pattern = '%'+nickname_contains+'%'
            query = Trainer.query.filter(Trainer.nickname.like(pattern)).limit(limit).offset(offset)
            return trainer_schemas.dumps(query.all())

    except NoResultFound:
        return jsonify([])

def get_trainer_by_email(email):
    try:
        return Trainer.query.filter_by(email=email).one()
    except:
        return None

def post_trainer():
    try:
        json = request.get_json()
    except:
        return ParsingError("Failed to parse JSON body")

    if type(json) is not dict:
        return ParsingError("Expected JSON object as body")

    try:
        nickname = json["nickname"]
        first_name = json["first_name"]
        last_name = json["last_name"]
        email = json["email"]
        password = json["password"]
        team = json["team"]

        trainer = Trainer(
                nickname=nickname,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                team=team
                )

        db.session.add(trainer)
        db.session.commit()

        return trainer_schema.dump(trainer)
    except InvalidTeam:
        return ParsingError("Field team is invalid")
    except KeyError:
        return ParsingError("Missing JSON object fields")
    except IntegrityError:
        return ConflictingResources("Trainer with the same nickname or email already exists", http_code=500)

def auth_trainer():
    try:
        auth = request.get_json()
    except:
        return ParsingError("Failed to parse JSON body")

    if type(auth) is not dict:
        return ParsingError("Expected JSON object as body")

    try:
        email = auth["email"]
        password = auth["password"]
    except KeyError:
        return AuthenticationFailure("Login required")

    trainer = get_trainer_by_email(email)
    if not trainer:
        return AuthenticationFailure("Trainer not found")

    if trainer and check_password_hash(trainer.password, password):
        token = jwt.encode(
                {
                    "username": trainer.nickname,
                    "exp": datetime.datetime.now() + datetime.timedelta(hours=12)
                },
                app.config["SECRET_KEY"])
        return jsonify(
                {
                    "id": trainer.id,
                    "token": token
                })

    return AuthenticationFailure("Invalid login")
