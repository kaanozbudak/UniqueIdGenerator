# Unique ID controller
from generator.controllers.base.api import BaseParameterController
from . import handler


class UniqueIdController(BaseParameterController):
    handler = handler.UniqueIdHandler
