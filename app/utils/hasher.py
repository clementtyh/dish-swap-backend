import bcrypt
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