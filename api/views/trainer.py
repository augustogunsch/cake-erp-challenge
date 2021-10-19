from sqlalchemy.exc import NoResultFound, IntegrityError
from api.models.trainer import Trainer, trainer_schema, trainer_schemas, InvalidTeam
from api.app import db
from api.app import app
from flask import request, jsonify
from .errors import *
from .parse_args import parse_limit, parse_offset, ParsingException, parse_json_obj
from werkzeug.security import check_password_hash
import datetime
import jwt

def get_trainer(id):
    try:
        trainer = Trainer.query.get(id)
        if trainer is None:
            return ("", 404)
        return trainer_schema.dump(trainer)
    except:
        return ("", 404)

def get_trainers():
    args = request.args

    try:
        limit = parse_limit()
        offset = parse_offset()
    except ParsingException as e:
        return ParsingError(e.message)

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
        json = parse_json_obj()

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

        return (trainer_schema.dump(trainer), 201)
    except ParsingException as e:
        return ParsingError(e.message)
    except InvalidTeam:
        return ParsingError("Field team is invalid")
    except KeyError:
        return ParsingError("Missing JSON object fields")
    except IntegrityError:
        return ConflictingResources("Trainer with the same nickname or email already exists")

def auth_trainer():
    try:
        auth = parse_json_obj()
        email = auth["email"]
        password = auth["password"]
    except ParsingException as e:
        return ParsingError(e.message)
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
                app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify(
                {
                    "id": trainer.id,
                    "token": token
                })

    return AuthenticationFailure("Invalid login")
