import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')

logger = logging.getLogger(name='test')
logger.setLevel(logging.ERROR)
