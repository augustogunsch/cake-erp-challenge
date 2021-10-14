from .trainer import Trainer
import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_trainers_table(self):
        con = sqlite3.connect(self.db_file)

        con.execute("""
            CREATE TABLE IF NOT EXISTS Trainers
            (
                id INT UNSIGNED UNIQUE,
                nickname TINYTEXT PRIMARY KEY,
                first_name TINYTEXT,
                last_name TINYTEXT,
                email TINYTEXT,
                password TINYTEXT,
                team TINYTEXT,
                pokemons_owned INT UNSIGNED
            )
        """)

        con.commit()
        con.close()

    def __get_trainers(self, sql):
        con = sqlite3.connect(self.db_file)
        trainers = []
        for row in con.execute(*sql):
            trainers.append(Trainer(*row).__dict__)
        con.close()
        return trainers

    def get_trainer_by_nickname(self, nickname, limit, offset):
        return self.__get_trainers(("SELECT * FROM Trainers WHERE nickname = ? LIMIT ? OFFSET ?", (nickname, limit, offset)))

    def get_trainers_by_nickname_contains(self, contains, limit, offset):
        return self.__get_trainers(("SELECT * FROM Trainers WHERE nickname LIKE ? LIMIT ? OFFSET ?", ("%" + contains + "%", limit, offset)))

    def insert_trainer(self, trainer):
        con = sqlite3.connect(self.db_file)

        con.execute("INSERT INTO Trainers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (trainer.id, trainer.nickname,
            trainer.first_name, trainer.last_name,
            trainer.email, trainer.password,
            trainer.team, trainer.pokemons_owned)
        )

        con.commit()
        con.close()

db = Database("database.db")
