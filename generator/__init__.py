import os
import time

from dotenv import load_dotenv

__version__ = '1.0.0.0'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True

CONFIGURATION_FILE = os.getenv('CONFIGURATION_FILE', 'conf/config.env')
assert CONFIGURATION_FILE is not None, ("""
Couldn't find CONFIGURATION_FILE in environment variable, set the variables before imports.

    >>> import os
    >>> os.environ.setdefault('CONFIGURATION_FILE', 'config/config.env')
    >>> 
    >>> from flow import *
""")
ENV_PATH = os.path.join(BASE_DIR, CONFIGURATION_FILE)
load_dotenv(dotenv_path=ENV_PATH)

# Setup timezone after set environment variable 'TZ'
time.tzset()

__authors__ = """
Generator
~~~~~~~~~~~~~~~~~~
Author:
- Kaan Ozbudak
"""

__info__ = "{}\nversion: {}".format(__authors__, __version__)
