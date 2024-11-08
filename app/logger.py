import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(module)s.%(funcName)s:%(lineno)d: %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)

    return logger
