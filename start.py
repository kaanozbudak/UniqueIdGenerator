import argparse
import logging
import os
from logging.handlers import RotatingFileHandler

logging.basicConfig(  # noqa
    level=logging.INFO,
    format="[%(asctime)s]:%(levelname)s %(name)s :%(module)s/%(funcName)s,%(lineno)d: %(message)s",
    handlers=[
        RotatingFileHandler('/tmp/generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('server')

parser = argparse.ArgumentParser(description='Generator')
parser.add_argument(
    '-c',
    '--config-file',
    type=str,
    dest='config',
    help='Config file path',
    default='conf/config.env'
)

args = parser.parse_args()

if __name__ == '__main__':
    os.environ.setdefault('CONFIGURATION_FILE', args.config)

    from generator import __info__ as info
    from generator.app import start

    print(info, end="\n\n")
    start()
