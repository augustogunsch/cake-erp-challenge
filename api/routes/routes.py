from api.app import app
from api.views import trainer, pokemon_owned, helper, errors
from flask import request
import asyncio

@app.route("/trainer/<int:trainerId>/", methods=["GET"])
def route_get_trainer(trainerId):
    return trainer.get_trainer(trainerId)

@app.route("/trainer/", methods=["GET"])
def route_get_trainers():
    return trainer.get_trainers()

@app.route("/trainer/", methods=["POST"])
def route_create_trainer():
    return trainer.post_trainer()

@app.route("/trainer/authenticate", methods=["POST"])
def route_auth_trainer():
    return trainer.auth_trainer()

@app.route("/trainer/<int:trainerId>/pokemon", methods=["GET"])
def route_get_pokemons_owned(trainerId):
    return asyncio.run(pokemon_owned.get_pokemons_owned(trainerId))

@app.route("/trainer/<int:trainerId>/pokemon", methods=["POST"])
@helper.token_required
def route_post_pokemons_owned(trainer, trainerId):
    if trainer.id != trainerId:
        return errors.ForbiddenError("Trainer id mismatch")
    return pokemon_owned.post_pokemon_owned(trainerId)

@app.route("/trainer/<int:trainerId>/pokemon/<int:pokemonId>", methods=["GET"])
def route_get_pokemon_owned(trainerId, pokemonId):
    return pokemon_owned.get_pokemon_owned(trainerId, pokemonId)

@app.route("/trainer/<int:trainerId>/pokemon/<int:pokemonId>", methods=["DELETE"])
@helper.token_required
def route_delete_pokemon_owned(trainer, trainerId, pokemonId):
    if trainer.id != trainerId:
        return errors.ForbiddenError("Trainer id mismatch")
    return pokemon_owned.delete_pokemon_owned(trainer, pokemonId)
