import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI

from app.core.logger import setup_logging
from app.utils.path_utils import PathUtils

if TYPE_CHECKING:
    from pathlib import Path

setup_logging()

LOGGER = logging.getLogger(__name__)

app = FastAPI()

# hardcoded path for testing
PATH = "/Users/ur/Downloads/E-commerce-project-springBoot-master2"

@app.get("/")
async def read_root():
    # Validate path
    path_utils = PathUtils(PATH)
    path: Path = path_utils.validate_project_structure()

    return(
        {
            "PATH" : PATH,
            "Validation" : True,
            "Project ROOT" : path,
        }
    )
