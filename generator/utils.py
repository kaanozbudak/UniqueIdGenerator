import os
import logging
import csv
from datetime import datetime
import hashlib
import random
import uuid

logger = logging.getLogger('utils')


class InvalidConfigKey(Exception):
    pass


class Config:
    """
    Config
    ~~~~~~

    Environment variable parser
    """

    def __getitem__(self, item: str) -> str:
        """
        Call when objects instance has request to get variable as item

        Usage:
        ~~~~~
        >>> import os; os.environ['test__getitem__'] = 'test-value'
        >>> config = Config()
        >>> config['test__getitem__']
        'test-value'

        >>> import uuid; unique_key = str(uuid.uuid4())
        >>> try:
        ...     config[unique_key]
        ... except InvalidConfigKey:
        ...      # We cannot see the value of unique value, so change exception message
        ...      print('"INVALID_KEY" does not set as environment variable.')
        "INVALID_KEY" does not set as environment variable.

        :type item: str
        :param item: The key you request to search in environment variable keys
        :return: Value of given environment variable key
        """
        try:
            return os.environ[item]
        except KeyError:
            raise InvalidConfigKey('"%s" does not set as environment variable.' % item)

    def __getattr__(self, item: str) -> str:
        """
        Call when objects instance has request to get variable as attribute

        Usage:
        ~~~~~~
        >>> import os; os.environ['test__getattr__'] = 'test-value'
        >>> config = Config()
        >>> config.test__getattr__
        'test-value'

        :type item: str
        :param item: The key you request to search in environment variable keys
        :return: Value of given environment variable key
        """
        return self.__getitem__(item)

    @staticmethod
    def get(key: str, default: str = None) -> str:
        """
        Call when object itself has request to get environment variable with/without defining class instance

        Usage:
        ~~~~~~
        >>> import os; os.environ['test_get'] = 'test-value'
        >>> Config.get('test_get')
        'test-value'

        >>> Config.get('test_not_exists_key')

        >>> Config.get('test_not_exists_key', default='a default test value')
        'a default test value'

        :type default: str
        :type key: str
        :param key: The key you request to search in environment variable keys
        :param default: Default value if key does not found int environment variables
        :return: Value of given environment variable key
        """
        return os.getenv(key, default)

    def __setitem__(self, key: str, value: str) -> None:
        """
        Call when request to set an environment variables with an objects instance as item

        Usage:
        ~~~~~~
        >>> config = Config()
        >>> config['test__setitem__'] = 'test-value'
        >>> import os; os.getenv('test__setitem__')
        'test-value'

        :type key: str
        :type value: str
        :param key: The key you want to set as environment variable
        :param value: Value to be stored in given environment variable with given key
        :return: None
        """
        if not isinstance(value, str):
            value = str(value)

        os.environ[key] = value

    def __setattr__(self, key: str, value: str) -> None:
        """
        Call when request to set an environment variables with an objects instance as attribute

        Usage:
        ~~~~~~
        >>> config = Config()
        >>> config.test__setattr__ = 'test-value'
        >>> import os; os.getenv('test__setattr__')
        'test-value'

        :type key: str
        :type value: str
        :param key: The key you want to set as environment variable
        :param value: Value to be stored in given environment variable with given key
        :return: None
        """
        self.__setitem__(key, value)

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Call when request to set an environment variables with/without defininig class instance

        Usage:
        ~~~~~~
        >>> config = Config()
        >>> Config.set('test_set', 'test-value')
        >>> import os; os.getenv('test_set')
        'test-value'

        :type key: str
        :type value: str
        :param key: The key you want to set as environment variable
        :param value: Value to be stored in given environment variable with given key
        :return: None
        """
        os.environ[key] = value


def format_date(date: datetime, fmt="%d/%m/%Y %H:%M:%S") -> str:
    """
    Utility for formatting given date

    >>> date = datetime(year=2020, month=10, day=4, hour=14, minute=45, second=39)
    >>> format_date(date)
    '04/10/2020 14:45:39'

    >>> format_date(date, fmt="%d/%m/%Y")
    '04/10/2020'

    :param date:
    :param fmt:
    :return:
    """
    return date.strftime(fmt)


def get_mongo_data(collection, start_time, end_time, temp_filter, many=True):
    from generator.helpers import Mongo

    mongo = Mongo(collection=collection)
    query_date = {
        "date": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    query_type = "query." + temp_filter
    query_filters = {
        "_id": 0,
        query_type: 1,
        "date": 1
    }
    if many:
        query_result = mongo.find(query_date, query_filters)
    else:
        query_result = mongo.find_one(query_date, query_filters)

    found = mongo.to_json(query_result)

    return found


def read_csv(path):
    hash_code = ''
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            hash_code = row[0]

    return hash_code


def clear_data():
    from generator.helpers import Mongo, Redis
    config = Config()
    # Mongo DB
    collection = config.get('MONGO_HASH')

    mongo = Mongo(collection=collection)

    # Redis DB
    redis = Redis(host=config.get('REDIS_HOST'),
                  port=config.get('REDIS_PORT'),
                  db=config.get('REDIS_DB'))

    mongo.collection.drop()
    redis.delete_all_keys()


def generate_new_hash_code(code):
    return hashlib.md5((code + str(random.getrandbits(32))).encode()).hexdigest()


def generate_unique_id():
    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())
    id3 = str(uuid.uuid4())
    unique_id_list = [id1, id2, id3]
    return unique_id_list
