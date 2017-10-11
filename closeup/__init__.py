import logging

logger = logging.getLogger()
handler = logging.FileHandler('closeup.log', mode='w')
formatter = logging.Formatter('%(levelname)-8s %(message)s')
    #'%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('Starting closeup module.')

#from . import main
from .main import main

