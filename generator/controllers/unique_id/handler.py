# Unique Id Handlers
from generator.controllers.base.handler import BaseHandler
from generator.helpers import Mongo


class UniqueIdHandler(BaseHandler):
    def handle(self) -> (list, dict):
        try:
            print('kaan')
            collection = self.config.get('MONGO_ID')
            mongo = Mongo(collection=collection)
            page = self.filters.get('page', 1)
            row_count = self.filters.get('row_count', 5)

            self.total = mongo.collection.count()

            result = {
                'name': 'kaan'
            }

        except Exception as ex:
            result = []

        return result
