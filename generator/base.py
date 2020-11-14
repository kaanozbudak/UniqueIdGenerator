from generator.utils import Config


class _Base(type):
    """
    BaseMetaClass metaclass for subclasses

    When add this class as metaclass to any subclass, each subclasses will have following attrs as default

    - `config`: Environment variable parser

    Usage:
    ~~~~~~

    >>> class SubClass(_Base):
    ...     pass
    >>> sub = SubClass()
    >>> hasattr(sub, 'config')
    True

    """

    def __new__(mcs, *args, **kwargs):
        instance = super().__new__(mcs, *args, **kwargs)
        instance.config = Config()
        return instance
