from functools import wraps
from flask import request
from api.app import app
from .fetch import get_trainer_by_nick_fail, NotFound
from .errors import AuthenticationFailure
import jwt

# autenticação do trainer (decorator)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers["authorization"]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            trainer = get_trainer_by_nick_fail(data["username"])
        except (TypeError, KeyError):
            return AuthenticationFailure("JWT token required")
        except NotFound:
            return AuthenticationFailure("Trainer not found")
        except:
            return AuthenticationFailure("JWT token is invalid or expired")

        return f(trainer, *args, **kwargs)
    return decorated

