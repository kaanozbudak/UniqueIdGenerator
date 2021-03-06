from time import sleep
from generator.helpers import Mongo, TimeStamp
from generator.utils import Config, format_date

config = Config()
collection = config.get('MONGO_HASH')
mongo = Mongo(collection=collection)


def get_data():
    temp = 0
    while True:
        count = mongo.count({})
        # yield data
        ts = TimeStamp()

        if temp != count or temp == 0:
            yield "<li>Time: " + str(format_date(ts.to_datetime())) + " -- " + "Total Count: " + str(
                count) + "</li>" + "<br><br>"
        sleep(2)
        temp = count
