from time import sleep
from generator.helpers import Mongo, TimeStamp
from generator.utils import Config, format_date

config = Config()
collection = config.get('MONGO_HASH')
mongo = Mongo(collection=collection)


def get_data():
    while True:
        count = mongo.count({})
        # yield data
        ts = TimeStamp()

        yield "<li>Time: " + str(format_date(ts.to_datetime())) + " -- " + "Total Count: " + str(
            count) + "</li>" + "<br><br>"
        # yield "Count: " + str(count) + " --- Time ----> " + str(ts.to_datetime().strftime('%X')) + "<br><br>"
        sleep(2)
