import logging
import json

from flask import request
from flask_restful import Resource

from generator import exceptions
from generator.utils import Config

logger = logging.getLogger('api')


class BaseController(Resource):
    _data = dict()
    _total = 0
    _status = 200

    def __init__(self):
        super().__init__()
        # NOTE: DO NOT use metaclass in generator.base, there has multiple meta class issue
        self.config = Config()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def code(self):
        return self.__class__.__name__

    def success(self):
        result = {
            "code": self.code,
            "status": self.status,
            "result": self.data,
            "total": self.total
        }
        return result

    def error(self, error):
        result = {
            "code": self.code,
            "status": self.status,
            "result": error,
            "total": self.total
        }
        return result

    def info(self, message):
        result = {
            "code": self.code,
            "status": self.status,
            "result": message,
            "total": self.total
        }
        return result

    def get(self):
        return self.info(message="Only POST method allowed.")

    def post(self):
        return self.success()


class BaseParameterController(BaseController):
    filters = dict()
    handler = None

    def get_handler(self):
        assert self.handler is not None, (
            "'{}' should have at least one handler".format(self.code)
        )
        return self.handler

    def prepare_filters(self, request_filters):
        assert isinstance(request_filters, dict), (
            "Request body 'filter' should be typeof object."
        )
        assert isinstance(self.filters, dict), (
            "'filters' type should be dictionary in class '{}'".format(self.code)
        )

        return {
            **request_filters,
            **self.filters
        }

    def post(self):
        # Multiple try-catch block for customizing error message!
        try:
            request_data: dict = json.loads(request.data.decode('utf-8'))
            request_filters = request_data.get('filter')
        except json.decoder.JSONDecodeError as ex:
            logger.exception(str(ex))
            self.status = 404
            return self.error(error='Wrong request body format! Error: ' + str(ex)), self.status

        try:
            prepared_filters = self.prepare_filters(request_filters)
        except Exception as ex:
            logger.exception(str(ex))
            self.status = 404
            return self.error(error="Wrong filters! Error: " + str(ex)), self.status

        try:
            handler = self.get_handler().__call__(**prepared_filters)
            self.data = handler.handle()
            self.total = handler.total
            return self.success(), self.status
        except exceptions.NotFoundError as ex:
            logger.exception(str(ex))
            self.status = 404
            return self.error(error=": " + str(ex)), self.status
        except Exception as ex:
            logger.exception(str(ex))
            self.status = 500
            return self.error(error="Error on handlers! Error: " + str(ex)), self.status


class SiteMapController(BaseController):
    def __init__(self):
        from flask import url_for
        from generator.urls import app
        links = []
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and self.has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append({
                    "url": url,
                    "controller": rule.endpoint
                })
        self._data = {
            "message": "[ CURRENT AVAILABLE LINKS ]",
            "links": links,
        }

    @staticmethod
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    def get(self):
        return self.success()
