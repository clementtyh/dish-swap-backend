import os

from motor.motor_asyncio import AsyncIOMotorClient


DB_URI = os.getenv("DB_URI")
CERT_FILE_PATH = os.getenv("CERT_FILE_PATH")


class MongoDBConnector:
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = AsyncIOMotorClient(
                DB_URI,
                tls=True,
                tlsCertificateKeyFile=CERT_FILE_PATH
            )
        return cls.client