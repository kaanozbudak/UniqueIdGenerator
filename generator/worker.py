from generator.helpers import Mongo, Redis, TimeStamp
from generator.utils import Config, read_csv, clear_data, generate_new_hash_code, generate_unique_id, format_date
import sys
import time


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

        # set recursion limit if do not system throw exception like maximum recursion dept
        sys.setrecursionlimit(10 ** 9)
        # clear data
        clear_data()

        # start generate
        self.generate_data()

    def generate_data(self):

        initial_code = read_csv(self.config.get('CSV_PATH'))

        loop_cycle_time = input('How many seconds do you want to generate\n')
        end_time = time.time() + int(loop_cycle_time)

        initial_unique_id_list = generate_unique_id()
        self.mongo_insert(initial_code, None, initial_unique_id_list)
        self.generate_hash_codes(initial_code)
        ts = TimeStamp()
        print('--------------')
        print("Start Time:" + " -- " + str(format_date(ts.to_datetime())))
        flag = True
        while flag:
            redis_pop = self.redis.right_pop('hash')
            for key in redis_pop:
                self.generate_hash_codes(key)
                if time.time() > end_time:
                    ts = TimeStamp()
                    print("End Time:" + " -- " + str(format_date(ts.to_datetime())))
                    flag = False
                    break
        count = self.mongo.count({})
        print('--------------')
        print("Total Count: " + str(count))
        print('--------------')
        print('How many seconds it worked: ' + str(loop_cycle_time))

    def generate_hash_codes(self, parent_hash_code):
        first_new_hash_code = generate_new_hash_code(parent_hash_code)
        second_new_hash_code = generate_new_hash_code(parent_hash_code)

        first_unique_id_list = generate_unique_id()
        second_unique_id_list = generate_unique_id()

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


Generator()
