# Unique Id Handlers
from generator.controllers.base.handler import BaseHandler
from generator.helpers import Mongo


class UniqueIdHandler(BaseHandler):
    def handle(self) -> (list, dict):
        try:
            collection = self.config.get('MONGO_ID')
            mongo = Mongo(collection=collection)
            # pagination
            page = self.filters.get('page', 1)
            row_count = self.filters.get('row_count', 5)

            self.total = mongo.collection.count()

            _result = mongo.find({}, {'_id': 0})
            result = mongo.to_json(_result)
            print(result)
        except Exception as ex:
            print("Exception: ", ex)
            result = []

        return result
