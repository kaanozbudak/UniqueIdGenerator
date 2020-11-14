from calendar import monthrange
from datetime import datetime, timedelta
from time import mktime

__all__ = (
    'TimeStamp',
)


class TimeStamp:
    """
    TimeStamp
    ~~~~~~~~~

    >>> ts = TimeStamp(1578302868) # Monday, January 6, 2020 12:27:48 PM GMT+03:00
    >>> ts.start_day
    1578258000
    >>> ts.end_day
    1578344399
    >>> ts.start_week
    1578258000
    >>> ts.end_week
    1578862799
    >>> ts.start_month
    1577826000
    >>> ts.end_month
    1580504399
    >>> ts.to_datetime()
    datetime.datetime(2020, 1, 6, 12, 27, 48)
    >>> ts.to_epoch()
    1578302868

    >>> ds = TimeStamp(datetime(year=2011, month=7, day=14, hour=6, minute=43, second=35))
    >>> ds.to_datetime()
    datetime.datetime(2011, 7, 14, 6, 43, 35)
    >>> ds.to_epoch()
    1310615015
    """

    def __init__(self, timestamp: (int, float, datetime) = None):
        """
        Timestamp helpers

        :param timestamp: timestamp in shape of epoch or datetime object
        """
        if timestamp is None:
            timestamp = datetime.now()

        if isinstance(timestamp, datetime):
            self._timestamp = timestamp
        else:
            # noinspection PyTypeChecker
            self._timestamp = datetime.fromtimestamp(timestamp)

    @staticmethod
    def _start_day(ts: datetime) -> int:
        return int(ts.replace(microsecond=0, second=0, minute=0, hour=0).timestamp())

    @staticmethod
    def _end_day(ts: datetime) -> int:
        return int(ts.replace(microsecond=999999, second=59, minute=59, hour=23).timestamp())

    def _start_week(self, ts: datetime) -> int:
        start = ts - timedelta(days=ts.weekday())
        return self._start_day(start)

    def _end_week(self, ts: datetime) -> int:
        end = ts + timedelta(days=6) - timedelta(days=ts.weekday())
        return self._end_day(end)

    def _start_month(self, ts: datetime) -> int:
        ts = ts.replace(day=1)
        return self._start_day(ts)

    def _end_month(self, ts: datetime) -> int:
        _, day = monthrange(year=ts.year, month=ts.month)
        ts = ts.replace(day=day)
        return self._end_day(ts)

    def to_datetime(self) -> datetime:
        """Datetime representation of given timestamp"""
        return self._timestamp

    def to_epoch(self) -> int:
        """Epoch time representation of given timestamp"""
        return int(mktime(self._timestamp.timetuple()))

    @property
    def start_day(self):
        """12:00:00 AM for given timestamp"""
        return self._start_day(self._timestamp)

    @property
    def end_day(self):
        """11:59:59 PM for given timestamp"""
        return self._end_day(self._timestamp)

    @property
    def start_week(self):
        """Monday 12:00:00 AM for given timestamp"""
        return self._start_week(self._timestamp)

    @property
    def end_week(self):
        """Sunday 11:59:59 PM for given timestamp"""
        return self._end_week(self._timestamp)

    @property
    def start_month(self):
        """Day_1 12:00:00 AM for given timestamp"""
        return self._start_month(self._timestamp)

    @property
    def end_month(self):
        """Day_28-31 Sunday 11:59:59 PM for given timestamp"""
        return self._end_month(self._timestamp)
