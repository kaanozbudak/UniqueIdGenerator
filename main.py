from time import sleep

from generator.helpers import Mongo, TimeStamp, Redis
from generator.utils import Config, read_csv
import hashlib
import random
import sys

config = Config()
collection = config.get('MONGO_HASH')
mongo = Mongo(collection=collection)
redis = Redis(host=config.get('REDIS_HOST'), port=config.get('REDIS_PORT'), db=config.get('REDIS_DB'))
sys.setrecursionlimit(10 ** 9)


def generator():
    first_code = read_csv('/Users/kaanozbudak/Documents/freelance/UniqueIdGenerator/hashed_code.csv')

    # initialize data
    mongo_insert(first_code, None)
    generate_hash_codes(first_code)

    while True:
        redis_pop = redis.right_pop('hash')
        for key in redis_pop:
            generate_hash_codes(key)


def generate_hash_codes(parent_hash_code):
    first_new_hash_code = generate_new_code(parent_hash_code)
    second_new_hash_code = generate_new_code(parent_hash_code)

    mongo_insert(first_new_hash_code, parent_hash_code)
    mongo_insert(second_new_hash_code, parent_hash_code)


def generate_new_code(code):
    return hashlib.md5((code + str(random.getrandbits(32))).encode()).hexdigest()


def mongo_insert(hash_code, hash_parent):
    if hash_parent:
        redis.insert_right_push('hash', hash_code)
    mongo.insert(
        {
            "hash_code": hash_code,
            "hash_parent": hash_parent,
            "unique_id": [],
            "created_at": TimeStamp().to_epoch()
        }
    )


# clear data
mongo.collection.drop()
redis.delete_all_keys()
# run
generator()
