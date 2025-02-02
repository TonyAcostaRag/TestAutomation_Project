import logging


def logIntoFile(message, level=logging.INFO):
    filename = 'test.log'
    logger = logging.getLogger(filename)
    logger.setLevel(level)

    fileHandler = logging.FileHandler('ReportingAndLogging/' + filename.format(filename), mode='a')
    fileHandler.setLevel(level)

    fileHandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s',
                                               datefmt='%Y %B %d %a %I:%M:%S %p'))

    logger.addHandler(fileHandler)

    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)
