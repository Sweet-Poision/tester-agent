from pathlib import Path

from fastapi import FastAPI

from app.core.logger import get_logger
from app.core.project_scanner import check_permissions
from app.utils.path_utils import path_is_valid

LOGGER = get_logger()

app = FastAPI()

# hardcoded path for testing
PATH = "/Users/ur/Downloads/E-commerce-project-springBoot-master2"

@app.get("/")
async def read_root():
    # Validate path
    path_is_valid(PATH)

    folder = Path(PATH)

    # check permissions
    permission_status, message = check_permissions(folder)

    if not permission_status:
        LOGGER.error("Permission error: %s", message)
        return {"success": False, "error": message}

    LOGGER.info("Path %s is valid and has necessary permissions.", PATH)

    return(f"Path '{PATH}' is valid and has necessary permissions.")
