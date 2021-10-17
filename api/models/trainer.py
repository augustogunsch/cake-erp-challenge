from api.app import db, ma
from werkzeug.security import generate_password_hash
from enum import Enum

teams = (
 "Team Valor",
 "Team Instinct",
 "Team Mystic"
 )

class InvalidTeam(Exception):
    pass

# modelo do Trainer para o SQLAlchemy
class Trainer(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nickname = db.Column(db.String(20), nullable=False, index=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    team = db.Column(db.String(10), nullable=False)
    pokemons_owned = db.Column(db.Integer, default=0)

    def __init__(self, nickname, first_name, last_name, email, password, team):
        if team not in teams:
            raise InvalidTeam()
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.team = team


# schema do Marshmallow
class TrainerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nickname', 'first_name', 'last_name', 'email', 'team', 'pokemons_owned')

trainer_schema = TrainerSchema()
trainer_schemas = TrainerSchema(many=True)
