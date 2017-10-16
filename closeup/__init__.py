# -*- coding: UTF-8 -*-
import logging

logger = logging.getLogger('closeup')
logger.setLevel(logging.DEBUG)

# formatter
#formatter = logging.Formatter('%(levelname)-8s %(message)s')
#formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
formatter = logging.Formatter('%(filename)s:%(lineno)d %(levelname)s - %(message)s','%m-%d %H:%M:%S')
#formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')

# file
file_handler = logging.FileHandler('closeup.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# add handlers
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

#logger.debug('Starting closeup module.')

#from . import main
from .main import main
from .structure import Name, Register

__version__ = '0.1.0'
