import bcrypt
from exceptions.user_exceptions import LoginPasswordDoesNotMatchException

def hash_password(password: str):
    try:
        password = password.encode("utf-8")
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password, salt)

        return hashed_password
    
    except Exception as e:
        print(e)
        raise


def validate_password(challenge_password: str, hashed_password: str):
    try:
        challenge_password = challenge_password.encode("utf-8")
        hashed_password = hashed_password.encode("utf-8")
        if not bcrypt.checkpw(challenge_password, hashed_password):
            raise LoginPasswordDoesNotMatchException

    except Exception as e:
        print(e)
        raise