# logger.py
import logging
import time

logging.basicConfig(filename=f'./logs/log{time.time()}.txt', level=logging.INFO)

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger