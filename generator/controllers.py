from time import sleep

from generator.helpers import Mongo, TimeStamp
from generator.utils import Config, read_csv

config = Config()
collection = config.get('MONGO_HASH')
mongo = Mongo(collection=collection)


def get_data():
    while True:
        results = mongo.count(
            {}
        )

        # yield data

        ts = TimeStamp()
        yield "Count: " + str(results) + " --- Time ----> " + str(ts.to_datetime().strftime('%X')) + "<br><br>"
        sleep(2)

        # for x in range(results):
        #     yield str.encode(str(results[x]) + "<br><br>" + str())
