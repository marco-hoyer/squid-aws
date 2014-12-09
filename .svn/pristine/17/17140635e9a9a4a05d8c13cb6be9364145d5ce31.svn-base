from functools import wraps
from time import time
import logging


def timed(function):

    logger = logging.getLogger(__name__)

    @wraps(function)
    def wrapper(*args, **kwds):
        start = time()
        result = function(*args, **kwds)
        elapsed = time() - start
        logger.info("{0} took {1} s to finish".format(function.__name__, elapsed))
        return result

    return wrapper