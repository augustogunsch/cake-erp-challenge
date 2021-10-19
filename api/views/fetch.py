from api.models.trainer import Trainer
import requests
import json

class NotFound(Exception):
    def __init__(self, message):
        self.message = message

def get_or_not_found(callback):
    try:
        resource = callback()
        if resource is None:
            raise NotFound("Resource not found")
        return resource
    except:
        raise NotFound("Resource not found")

def get_trainer_fail(id):
    return get_or_not_found(lambda : Trainer.query.get(id))

def get_trainer_by_nick_fail(nickname):
    return get_or_not_found(lambda : Trainer.query.filter_by(nickname=nickname).one())

def get_pokemon_fail(trainer, id):
    return get_or_not_found(lambda : trainer.pokemons_list.filter_by(id=id).one())

# helper interno
def cant_fetch_error(pokemon):
    raise NotFound("Could not fetch data for pokemon with id {}".format(pokemon.pokemon_id))

# seguintes funções puxam informações da pokeapi
def set_pokemon_data(pokemon):
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon.pokemon_id))
        if response.status_code != 200:
            cant_fetch_error(pokemon)
        pokemon.pokemon_data = json.loads(response.text)
    except:
        cant_fetch_error(pokemon)

async def async_set_pokemon_data(session, pokemon):
    try:
        response = await session.get("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon.pokemon_id))
        if response.status != 200:
            cant_fetch_error(pokemon)
        pokemon.pokemon_data = json.loads(await response.text())
    except:
        cant_fetch_error(pokemon)
