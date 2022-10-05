
from logging import getLogger, INFO

# TODO add custom logger instead of uvicorn's logger
logger = getLogger("uvicorn")
logger.setLevel(INFO)
logger.info("logger initialized")
