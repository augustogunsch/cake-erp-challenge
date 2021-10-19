from api.models.pokemon_owned import pokemon_owned_schema, pokemon_owned_schemas, PokemonOwned
from api.app import db
from .parse_args import parse_limit, parse_offset, ParsingException, parse_json_obj
from .errors import ParsingError, FetchError, ConflictingResources
from .helper import *
from aiohttp import ClientSession
import asyncio
from sqlalchemy.exc import IntegrityError

def post_pokemon_owned(trainer_id):
    try:
        json = parse_json_obj()
        pokemon_id = json["pokemon_id"]
        name = json["name"]
        level = json["level"]
    except ParsingException as e:
        return ParsingError(e.message)
    except KeyError:
        return ParsingError("Missing JSON object fields")

    pokemon = PokemonOwned(
            name=name,
            level=level,
            pokemon_id=pokemon_id,
            trainer_id=trainer_id
            )

    try:
        set_pokemon_data(pokemon)

        db.session.add(pokemon)
        db.session.commit()
    except NotFound as e:
        return FetchError(e.message)
    except IntegrityError:
        return ConflictingResources("Trainer already has another pokemon with the same name")

    return (pokemon_owned_schema.dump(pokemon), 201)

async def get_pokemons_owned(trainer_id):
    try:
        limit = parse_limit()
        offset = parse_offset()
    except ParsingException as e:
        return ParsingError(e.message)

    try:
        trainer = get_trainer_fail(trainer_id)
    except NotFound:
        return "", 404

    pokemons = trainer.pokemons_list.limit(limit).offset(offset).all()

    async with ClientSession() as session:
        tasks = []
        for pokemon in pokemons:
            task = asyncio.create_task(async_set_pokemon_data(session, pokemon))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except NotFound as e:
            for task in tasks:
                task.cancel()
            return FetchError(e.message)

    # workaround pra bug do aiohttp, que pode gerar avisos de conexões abertas
    # ver documentação: https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    # será arrumado na versão 4.0.0, que ainda não saiu
    # issue no github: https://github.com/aio-libs/aiohttp/issues/1925
    await asyncio.sleep(0.250)

    return pokemon_owned_schemas.dumps(pokemons)

def get_pokemon_owned(trainer_id, pokemon_id):
    try:
        trainer = get_trainer_fail(trainer_id)
        pokemon = get_pokemon_fail(trainer, pokemon_id)
        set_pokemon_data(pokemon)
        return pokemon_owned_schema.dump(pokemon)
    except NotFound:
        return "", 404
    except HTTPError as e:
        return FetchError(e.message)
    except NotFound as e:
        return ParsingError(e.message)

def delete_pokemon_owned(trainer, pokemon_id):
    try:
        pokemon = get_pokemon_fail(trainer, pokemon_id)
        set_pokemon_data(pokemon)
        db.session.delete(pokemon)
        db.session.commit()
        return pokemon_owned_schema.dump(pokemon)
    except NotFound:
        return "", 404
    except HTTPError as e:
        return FetchError(e.message)
