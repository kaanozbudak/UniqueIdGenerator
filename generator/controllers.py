from datetime import datetime
from time import sleep
from generator.helpers import Mongo
from generator.utils import Config

config = Config()


def generator():
    c = 1
    collection = config.get('MONGO_ID')
    mongo = Mongo(collection=collection)
    while True:
        mongo.insert(
            {
                "name": c
            }
        )
        results = mongo.search({}, {'name': 1}, skip=c)
        for x in results:
            yield str.encode(str(x['name']) + '\n')
        # yield '[{}] Generated Id: {}\n'.format(datetime.now().strftime('%x %X'), c)
        # yield from results
        c += 1
        sleep(3)

