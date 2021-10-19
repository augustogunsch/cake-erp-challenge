import string
import random

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
SECRET_KEY = ''.join(random.choice(random_str) for _ in range(12))
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
