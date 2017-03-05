import logging


def setup_logger():
    root_logger = logging.getLogger('main')
    root_logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('main.log', 'w', 'utf-8')
    #handler.setFormatter = logging.Formatter('%(levelname)s:%(message)s')
    handler.setFormatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    root_logger.addHandler(handler)

    return root_logger