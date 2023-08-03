import logging


def get_logger(name: str, log_filename: str) -> logging.Logger:
    """
    Basic logger for tracking how much time user spent for each set of widgets.
    Writes into logfile.

    Args:
        name (str): logging name
        log_filename (str): file to save.

    Returns:
        logging.Logger: logger class
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
