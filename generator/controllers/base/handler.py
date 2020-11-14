from generator.base import _Base

from generator.helpers import Mongo


class BaseHandler(metaclass=_Base):
    _total = 0

    def __init__(self, **filters):
        self.filters = filters

    @property
    def start_time(self):
        start_time = self.filters.get('start_time', None)
        if start_time is not None and len(str(start_time)) > 10:
            start_time = int(str(start_time)[:10])
        return start_time

    @property
    def end_time(self):
        end_time = self.filters.get('end_time', None)
        if end_time is not None and len(str(end_time)) > 10:
            end_time = int(str(end_time)[:10])
        return end_time

    @property
    def time_method(self):
        return self.filters.get('time_method', "hour")

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    def paginated_data(self, result):
        # if data is not type of list, then data cannot be paginated
        if not isinstance(result, list):
            return result

        self.total = len(result)

        if self.page is not None:
            # page: 1, row_count: 10, => result[0: 10]
            # page: 2, row_count: 10, => result[10:20]
            # page: 3, row_count: 10, => result[20:30]
            # page: 4, row_count: 10, => result[30:40]
            # page: x, row_count: y , => result[(page-1)*row_count:page*row_count]

            page = int(self.page)
            row_count = int(self.row_count or 10)
            result = result[(page - 1) * row_count:page * row_count]
        return result

    def handle(self) -> (list, dict):
        raise NotImplementedError


class BaseMongoHandler(BaseHandler):
    def __init__(self, **filters):
        super().__init__(**filters)

    @property
    def mongo_instance(self):
        collection = "{}{}".format(self.config.get('MONGO_TARGET_COLLECTION_PREFIX'), self.job_type)
        return Mongo(collection=collection)

    def get_query_date(self, **kwargs):
        current = kwargs.get('current', False)
        start_time = kwargs.get('start_time', self.start_time)
        end_time = kwargs.get('end_time', self.end_time)
        job_type = kwargs.get('job_type', self.job_type)
        trend = kwargs.get('trend', self.trend)

        if current:
            if job_type == 'daily':
                start_time = end_time - 86400  # day before yesterday
            elif job_type == 'weekly':
                start_time = end_time - 86400 * 7  # week before last week
            elif job_type == 'monthly':
                start_time = end_time - 86400 * 30  # month before last month
        elif trend:
            if job_type == 'daily':
                end_time = end_time - 86400  # day before today
                start_time = end_time - 86400 * 2  # day before yesterday
            elif job_type == 'weekly':
                end_time = end_time - 86400 * 7  # week before this week
                start_time = end_time - 86400 * 7 * 2  # week before last week
            elif job_type == 'monthly':
                end_time = end_time - 86400 * 30  # month before this month
                start_time = end_time - 86400 * 30 * 2  # month before last month

        return {"date": {"$gte": start_time, "$lt": end_time}}

    def handle(self) -> (list, dict):
        return NotImplementedError
