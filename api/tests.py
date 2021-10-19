#!/bin/python3
from api.app import app, db
from api.models.trainer import Trainer
from api.models.pokemon_owned import PokemonOwned
from flask_testing import TestCase
import unittest

class MainTestCase(TestCase):

    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing.db"
        db.drop_all()
        db.create_all()
        trainers = (
            Trainer(
                nickname="jose",
                first_name="José",
                last_name="da Silva",
                email="josedasilva.2021@gmail.com",
                password="1234",
                team="Team Valor"
                ),
            Trainer(
                nickname="joao",
                first_name="João",
                last_name="Oliveira",
                email="joaooliveira@hotmail.com",
                password="senha",
                team="Team Instinct"
                ),
            Trainer(
                nickname="ricardo",
                first_name="Ricardo",
                last_name="Teixeira",
                email="ricardo.teixeira@gmail.com",
                password="ricardo",
                team="Team Mystic"
                ),
        )
        pokemons = (
            PokemonOwned(
                name="Fluffy",
                level=1,
                pokemon_id=12,
                trainer_id=1
                ),
            PokemonOwned(
                name="Dinossauro",
                level=1,
                pokemon_id=2,
                trainer_id=1
                ),
            PokemonOwned(
                name="Outro",
                level=1,
                pokemon_id=4,
                trainer_id=1
                ),
        )
        db.session.add_all(trainers)
        db.session.add_all(pokemons)
        db.session.commit()

        self.client = app.test_client()

        login = {
                "email": "joaooliveira@hotmail.com",
                "password": "senha",
        }
        auth = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_200(auth)
        self.token_joao = auth.get_json()["token"]

        return app

    def test_post_trainer(self):
        trainer = {
            "nickname": "rodrigro",
            "first_name": "Ricardo",
            "last_name": "Lopes",
            "email": "rlopes@outlook.com",
            "password": "dummy",
            "team": "Team Mystic"
        }
        response = self.client.post("/trainer", json=trainer, follow_redirects=True)
        self.assert_status(response, 201)
        self.assertEqual(trainer["email"], response.get_json()["email"])

    def test_post_trainer_duplicate(self):
        trainer = {
            "nickname": "julio",
            "first_name": "Julio",
            "last_name": "Sobreiro",
            "email": "julho.sob@yahoo.com",
            "password": "0987",
            "team": "Team Mystic"
        }
        self.client.post("/trainer", json=trainer, follow_redirects=True)
        response = self.client.post("/trainer", json=trainer, follow_redirects=True)
        self.assert_status(response, 409)

    def test_post_trainer_invalid_team(self):
        trainer = {
            "nickname": "cesar",
            "first_name": "Cesar",
            "last_name": "Pereira",
            "email": "cesereira@gmail.com",
            "password": "04031994",
            "team": "Team Inventado"
        }
        response = self.client.post("/trainer", json=trainer, follow_redirects=True)
        self.assert_400(response)

    def test_post_trainer_missing_fields(self):
        trainer = {}
        response = self.client.post("/trainer", json=trainer, follow_redirects=True)
        self.assert_400(response)

    def test_authenticate(self):
        login = {
                "email": "josedasilva.2021@gmail.com",
                "password": "1234",
        }
        response = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"id", response.data)
        self.assertIn(b"token", response.data)

    def test_authenticate_wrong(self):
        login = {
                "email": "josedasilva.2021@gmail.com",
                "password": "wrong_password",
        }
        response = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_401(response)

    def test_authenticate_not_found(self):
        login = {
                "email": "notrainer@withemail.com",
                "password": "dummy_password",
        }
        response = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_401(response)

    def test_authenticate_no_login(self):
        login = {}
        response = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_401(response)

    def test_get_trainers(self):
        response = self.client.get("/trainer", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"jose", response.data)
        self.assertIn(b"joao", response.data)
        self.assertIn(b"ricardo", response.data)

    def test_get_trainer_by_nickname(self):
        response = self.client.get("/trainer?nickname=jose", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"jose", response.data)

    def test_get_trainer_by_nickname_not_found(self):
        response = self.client.get("/trainer?nickname=somerandomnickname", follow_redirects=True)
        self.assert_200(response)
        self.assertEqual(response.data, b"[]")

    def test_get_trainer_by_nickname_contains(self):
        response = self.client.get("/trainer?nickname_contains=jo", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"jose", response.data)
        self.assertIn(b"joao", response.data)

    def test_get_trainer_by_nickname_contains_limit(self):
        response = self.client.get("/trainer?nickname_contains=jo&limit=1", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"jose", response.data)
        self.assertNotIn(b"joao", response.data)

    def test_get_trainer_by_nickname_contains_offset(self):
        response = self.client.get("/trainer?nickname_contains=jo&offset=1", follow_redirects=True)
        self.assert_200(response)
        self.assertNotIn(b"jose", response.data)
        self.assertIn(b"joao", response.data)

    def test_get_trainer_by_id(self):
        response = self.client.get("/trainer/1", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"jose", response.data)
        self.assertNotIn(b"joao", response.data)

    def test_get_trainer_by_id_not_found(self):
        response = self.client.get("/trainer/1000", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_get_pokemons(self):
        response = self.client.get("/trainer/1/pokemon", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"Fluffy", response.data)
        self.assertIn(b"Dinossauro", response.data)
        self.assertIn(b"Outro", response.data)
        self.assertIn(b"pokemon_data", response.data)

    def test_get_pokemons_trainer_not_found(self):
        response = self.client.get("/trainer/1000/pokemon", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_get_pokemons_limit(self):
        response = self.client.get("/trainer/1/pokemon?limit=1", follow_redirects=True)
        self.assert_200(response)
        self.assertIn(b"Fluffy", response.data)
        self.assertNotIn(b"Dinossauro", response.data)
        self.assertNotIn(b"Outro", response.data)

    def test_get_pokemons_offset(self):
        response = self.client.get("/trainer/1/pokemon?offset=1", follow_redirects=True)
        self.assert_200(response)
        self.assertNotIn(b"Fluffy", response.data)
        self.assertIn(b"Dinossauro", response.data)
        self.assertIn(b"Outro", response.data)

    def test_get_pokemon_by_id(self):
        response = self.client.get("/trainer/1/pokemon/2", follow_redirects=True)
        self.assert_200(response)
        self.assertNotIn(b"Fluffy", response.data)
        self.assertIn(b"Dinossauro", response.data)
        self.assertNotIn(b"Outro", response.data)
        self.assertIn(b"pokemon_data", response.data)

    def test_get_pokemon_by_id_not_found(self):
        response = self.client.get("/trainer/1/pokemon/1000", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_post_pokemon_no_auth(self):
        data = {
                "name": "Dummy",
                "level": 9,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/2/pokemon", json=data, follow_redirects=True)
        self.assert_401(response)

    def test_post_pokemon(self):
        data = {
                "name": "Dummy",
                "level": 2,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/2/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_status(response, 201)
        self.assertIn(b"Dummy", response.data)
        self.assertIn(b"pokemon_data", response.data)

    def test_post_pokemon_trainer_not_found(self):
        data = {
                "name": "Dummy",
                "level": 2,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/200/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_403(response)

    # adicionando pokemon pra outro trainer
    def test_post_pokemon_forbidden(self):
        data = {
                "name": "Dummy",
                "level": 2,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/1/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_403(response)

    def test_post_pokemon_no_species(self):
        data = {
                "name": "Dumb",
                "level": 2,
                "pokemon_id": 12000
        }
        response = self.client.post("/trainer/2/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_404(response)

    def test_delete_pokemon_trainer_not_found(self):
        response = self.client.delete("/trainer/200/pokemon/1", headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_403(response)

    def test_delete_pokemon_no_auth(self):
        data = {
                "name": "Dummier",
                "level": 2,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/2/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_status(response, 201)
        response = self.client.delete("/trainer/2/pokemon/{}".format(response.get_json()["id"]), follow_redirects=True)
        self.assert_401(response)

    def test_delete_pokemon_not_found(self):
        login = {
                "email": "joaooliveira@hotmail.com",
                "password": "senha",
        }
        auth = self.client.post("/trainer/authenticate", json=login, follow_redirects=True)
        self.assert_200(auth)
        token = auth.get_json()["token"]
        response = self.client.delete("/trainer/2/pokemon/1000", headers={"Authorization":token}, follow_redirects=True)
        self.assert_404(response)

    def test_delete_pokemon(self):
        data = {
                "name": "Dummier",
                "level": 2,
                "pokemon_id": 12
        }
        response = self.client.post("/trainer/2/pokemon", json=data, headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_status(response, 201)
        response = self.client.delete("/trainer/2/pokemon/{}".format(response.get_json()["id"]), headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_200(response)

    # deletando pokemon de outro trainer
    def test_delete_pokemon_forbidden(self):
        response = self.client.delete("/trainer/1/pokemon/1", headers={"Authorization":self.token_joao}, follow_redirects=True)
        self.assert_403(response)



if __name__ == "__main__":
    unittest.main()
