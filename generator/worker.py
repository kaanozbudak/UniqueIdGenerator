import uuid

from generator.helpers import Mongo, Redis
from generator.utils import Config, read_csv
import hashlib
import random
import sys


class Generator:
    def __init__(self):
        self.config = Config()

        # Mongo DB
        self.collection = self.config.get('MONGO_HASH')
        self.mongo = Mongo(collection=self.collection)

        # Redis DB
        self.redis = Redis(host=self.config.get('REDIS_HOST'),
                           port=self.config.get('REDIS_PORT'),
                           db=self.config.get('REDIS_DB'))

        # set recursion limit if do not system throw exceotion like maximum recursion dept
        sys.setrecursionlimit(10 ** 9)
        # clear data
        self.clear_data()

        # start generate
        self.generate_data()

    def generate_data(self):
        initial_code = read_csv(self.config.get('CSV_PATH'))

        # initialize data
        initial_unique_id_list = self.generate_unique_id()
        self.mongo_insert(initial_code, None, initial_unique_id_list)
        self.generate_hash_codes(initial_code)

        while True:
            redis_pop = self.redis.right_pop('hash')
            for key in redis_pop:
                self.generate_hash_codes(key)

    def generate_hash_codes(self, parent_hash_code):
        first_new_hash_code = self.generate_new_hash_code(parent_hash_code)
        second_new_hash_code = self.generate_new_hash_code(parent_hash_code)

        first_unique_id_list = self.generate_unique_id()
        second_unique_id_list = self.generate_unique_id()

        self.mongo_insert(first_new_hash_code, parent_hash_code, first_unique_id_list)
        self.mongo_insert(second_new_hash_code, parent_hash_code, second_unique_id_list)

    def mongo_insert(self, hash_code, hash_parent, unique_id_list):

        if hash_parent:
            self.redis.insert_right_push('hash', hash_code)
        self.mongo.insert(
            {
                "hash_code": hash_code,
                "hash_parent": hash_parent,
                "unique_id": unique_id_list,
            }
        )

    def generate_new_hash_code(self, code):
        return hashlib.md5((code + str(random.getrandbits(32))).encode()).hexdigest()

    def generate_unique_id(self):
        id1 = str(uuid.uuid4())
        id2 = str(uuid.uuid4())
        id3 = str(uuid.uuid4())
        unique_id_list = [id1, id2, id3]
        return unique_id_list

    def clear_data(self):
        self.mongo.collection.drop()
        self.redis.delete_all_keys()


Generator()
