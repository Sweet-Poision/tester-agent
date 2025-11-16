from pathlib import Path

from starlette.exceptions import HTTPException

from app.core.logger import get_logger

LOGGER = get_logger()

def path_is_valid(path: str) -> None:
    p = Path(path)
    if not p.exists():
        LOGGER.error("Invalid path: %s does not exist.", path)
        raise HTTPException(status_code=400, detail="Invalid Path")
    if not p.is_dir():
        LOGGER.error("Path is not a directory: %s", path)
        raise HTTPException(status_code=400, detail="Path is not a directory")

    LOGGER.info("Path %s is valid.", path)
