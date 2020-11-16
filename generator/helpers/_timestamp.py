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

    def to_datetime(self) -> datetime:
        """Datetime representation of given timestamp"""
        return self._timestamp

    def to_epoch(self) -> int:
        """Epoch time representation of given timestamp"""
        return int(mktime(self._timestamp.timetuple()))


