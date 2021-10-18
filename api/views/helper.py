from functools import wraps
from flask import request
from api.models.trainer import Trainer
from .errors import AuthenticationFailure
from api.app import app
import requests
import json
import jwt

class HTTPError(Exception):
    def __init__(self, message):
        self.message = message

class TrainerNotFound(Exception):
    pass

def get_trainer_fail(id):
    try:
        trainer = Trainer.query.get(id)
        if trainer is None:
            raise TrainerNotFound()
        return trainer
    except:
        raise TrainerNotFound()

def get_trainer_by_nick_fail(nickname):
    try:
        trainer = Trainer.query.filter_by(nickname=nickname).one()
        if trainer is None:
            raise TrainerNotFound()
        return trainer
    except:
        raise TrainerNotFound()

# authenticação do trainer (decorator)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers["authorization"]
            print(token)
            print(app.config["SECRET_KEY"])
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data["username"])
            trainer = get_trainer_by_nick_fail(data["username"])
        except (TypeError, KeyError):
            return AuthenticationFailure("JWT token required")
        except:
            return AuthenticationFailure("JWT token is invalid or expired")

        return f(trainer, *args, **kwargs)
    return decorated

# seguintes funções puxam informações da pokeapi
def set_pokemon_data(pokemon):
    response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon.pokemon_id))
    if response.status_code != 200:
        raise HTTPError("Could not fetch pokemon with id {}".format(pokemon.pokemon_id))
    pokemon.pokemon_data = json.loads(response.text)

async def async_set_pokemon_data(session, pokemon):
    response = await session.get("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon.pokemon_id))
    if response.status != 200:
        raise HTTPError("Could not fetch pokemon with id {}".format(pokemon.pokemon_id))
    pokemon.pokemon_data = json.loads(await response.text())
