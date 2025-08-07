import logging
from .config import get_rotating_handler

db_logger = logging.getLogger("db_logger")
db_logger.setLevel(logging.DEBUG)
db_logger.addHandler(get_rotating_handler("db.log"))

def log_query(sql, params=None, duration_ms=None):
    msg = f"QUERY: {sql}"
    if params:
        msg += f" | Params: {params}"
    if duration_ms:
        msg += f" | Time: {duration_ms:.2f}ms"
    db_logger.info(msg)

def log_db_error(error, context=None):
    msg = f"DB ERROR: {error}"
    if context:
        msg += f" | Context: {context}"
    db_logger.error(msg)

def log_db_event(event, detail=None):
    msg = f"{event}"
    if detail:
        msg += f" | Detail: {detail}"
    db_logger.info(msg)
