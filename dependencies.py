from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from .config import API_KEY
from .config import API_KEY_NAME
import logging
import logging.handlers
logger = logging.getLogger("uvicorn.access")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)):
    logger.info("Validando clave API")
    if api_key != API_KEY:
        logger.warning("Clave API no válida")
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
    logger.info("Clave API validada correctamente")
    return True
