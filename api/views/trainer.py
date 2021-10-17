from sqlalchemy.exc import NoResultFound, IntegrityError
from api.models.trainer import Trainer, trainer_schema, trainer_schemas, InvalidTeam
from api.app import db
from flask import request, jsonify

# função auxiliar
def error(code, type, message, http_code=400):
    return ({
            "code": code,
            "type": type,
            "message": message
    }, http_code)

def get_trainer(id):
    return trainer_schema.dump(Trainer.query.get(id))

def get_trainers():
    args = request.args

    try:
        limit = int(args.get("limit", -1))
        offset = int(args.get("offset", 0))
    except ValueError:
        return error(0, "ParsingError", "Couldn't parse parameter as integer")

    if limit < -1 or offset < 0:
        return error(1, "ParsingError", "Expected positive integer as parameter")

    nickname = args.get("nickname", "")
    nickname_contains = args.get("nickname_contains", "")

    try:
        if nickname:
            if nickname_contains:
                return error(2, "ConflictingParameters", "nickname and nickname_contains are mutually exclusive")

            query = Trainer.query.filter_by(nickname=nickname)
            return trainer_schemas.dumps(query.all())

        else:               # se nickname_contains também está vazio, retornará todos trainers
            pattern = '%'+nickname_contains+'%'
            query = Trainer.query.filter(Trainer.nickname.like(pattern))
            return trainer_schemas.dumps(query.all())

    except NoResultFound:
        return jsonify([])

def post_trainer():
    try:
        json = request.get_json()
    except:
        return error(3, "ParsingError", "Failed to parse JSON content")

    if type(json) is not dict:
        return error(4, "ParsingError", "Expected JSON object as content")

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
        return error(5, "ParsingError", "Field team is invalid")
    except KeyError:
        return error(6, "ParsingError", "Missing JSON object fields")
    except IntegrityError:
        return error(7, "ConflictingResource", "Trainer with the same nickname or email already exists", http_code=500)
