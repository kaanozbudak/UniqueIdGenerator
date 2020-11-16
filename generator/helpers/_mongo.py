from bson.json_util import dumps, loads
from pymongo import MongoClient

from generator.base import _Base

__all__ = (
    'Mongo',
    'to_json'
)


class Mongo(metaclass=_Base):
    def __init__(self, collection):
        try:
            if self.config.MONGO_ADDRESS_URI:
                self._client = MongoClient(self.config.MONGO_ADDRESS_URI)
                self.check_status()
                self._database = self._client[self.config.MONGO_DB_NAME]
            else:
                uri = 'mongodb://{username}:{password}@{host}:{port}/{database_name}'.format(
                    username=self.config.MONGO_USER,
                    password=self.config.MONGO_PASSWORD,
                    host=self.config.MONGO_HOST,
                    port=self.config.MONGO_PORT,
                    database_name=self.config.MONGO_DB_NAME,
                )
                self._client = MongoClient(uri)
                self.check_status()
                self._database = self._client.get_database(self.config.MONGO_DB_NAME)

            self._collection = self._database.get_collection(collection)
        except Exception as ex:
            raise Exception('Cannot connect mongo database! ' + str(ex))

    def check_status(self):
        self._client.server_info()

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self._database

    @property
    def collection(self):
        """Collection name for given database"""
        return self._collection

    def insert(self, data: dict):
        """Insert single dictionary to database"""
        self.collection.insert_one(data)

    def count(self, filter_):
        """Count documents by filter_"""
        return self.collection.count(filter_)

    def search(self, filter_, projection, to_json=True, skip=None, limit=None):
        """Find documents by filter_"""
        # page: 1, row_count: 10, skip

        found = self.collection.find(filter_, projection)
        if skip is not None:
            limit = int(limit) if limit else 10
            skip = (int(skip) - 1) * limit or 0

            found = found.skip(skip).limit(limit)

        if not found:
            found = []

        if to_json:
            return self.to_json(found)

        return found

    def find(self, query, parameters, to_json=True):
        """Find documents by query"""
        found = self.collection.find(query, parameters, no_cursor_timeout=True)

        if not found:
            found = []

        if to_json:
            return self.to_json(found)

        return found

    def find_one(self, query, parameters, to_json=True):
        """Find document by query"""
        found = self.collection.find_one(query, parameters)

        if not found:
            return {}

        if to_json:
            return self.to_json(found)

        return found

    @staticmethod
    def to_json(result):
        """Convert bson cursor object to json"""
        return loads(dumps(result))


def to_json(value):
    return loads(dumps(value))
