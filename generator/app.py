import logging

from generator.urls import app
from generator.utils import Config

config = Config()
logger = logging.getLogger('generator')


def start():
    logger.info("Running application")
    debug = int(config.get('DEBUG'))

    app.run(host=config.get('HOST'), port=config.get('PORT'), debug=bool(debug))
