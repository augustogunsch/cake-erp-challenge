from api.app import db, ma
from .trainer import *

class PokemonOwned(db.Model):
    __tablename__ = "pokemons_owned"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(50), unique=True, index=True, nullable=False)
    level = db.Column(db.Integer)
    pokemon_id = db.Column(db.Integer)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"), index=True)

    def __init__(self, name, level, pokemon_id, trainer_id):
        self.name = name
        self.level = level
        self.pokemon_id = pokemon_id
        self.trainer_id = trainer_id

class PokemonOwnedSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'level', 'pokemon_data')

pokemon_owned_schema = PokemonOwnedSchema()
pokemon_owned_schemas = PokemonOwnedSchema(many=True)
