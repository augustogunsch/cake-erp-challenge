from flask import request, jsonify
from app import app
from app.database import db

@app.route('/trainer', methods=['GET'])
def route_get_trainers():
    args = request.args

    try:
        limit = int(args.get("limit", 0))
        offset = int(args.get("offset", 0))
    except ValueError:
        return {
                "code": 1,
                "type": "Integer parsing error",
                "message": "Couldn't parse parameter as integer"
        }, 500

    if limit < 0 or offset < 0:
        return {
                "code": 2,
                "type": "Integer parsing error",
                "message": "Expected positive integer as parameter"
        }, 500

    limit_str = "LIMIT %d" % limit if "limit" in args else "" # gambiarra pra tornar o limite infinito por padrão

    nickname = args.get("nickname", "")
    nickname_contains = args.get("nickname_contains", "")

    if nickname and nickname_contains:
        return { 
                "code": 3,
                "type": "Invalid parameter",
                "message": "Parameters \"nickname\" and \"nickname_contains\" are mutually exclusive"
        }, 500

    if nickname:
        return jsonify(db.get_trainer_by_nickname(nickname, limit_str, offset))
    else:
        return jsonify(db.get_trainers_by_nickname_contains(nickname_contains, limit_str, offset))
