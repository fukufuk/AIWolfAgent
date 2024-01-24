import logging


def build_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
    )
    LOGGER = logging.getLogger(name)
    return LOGGER
