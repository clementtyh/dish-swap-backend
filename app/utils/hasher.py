import bcrypt
from exceptions.user_exceptions import InvalidPasswordException
from utils.logger import logger

def hash_password(password: str):
    try:
        password = password.encode("utf-8")
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password, salt)

        return hashed_password
    
    except Exception as e:
        logger.error(e)
        raise


def validate_password(challenge_password: str, hashed_password: str):
    try:
        challenge_password = challenge_password.encode("utf-8")
        hashed_password = hashed_password.encode("utf-8")
        if not bcrypt.checkpw(challenge_password, hashed_password):
            raise InvalidPasswordException

    except Exception as e:
        logger.error(e)
        raise