import logging
import os
import typing
from pathlib import Path

from starlette.exceptions import HTTPException

LOGGER = logging.getLogger(__name__)

class PathUtils:
    def __init__(self, root: str):
        self.root : Path = Path(root).resolve()
        self.src_dir : Path | None = None

    def validate_project_structure(self) -> Path:
        self._check_exists()
        self._check_is_directory()
        self._check_permissions()
        self._detect_project_root()

        LOGGER.info("Project structure validated for PATH %s\nProject found at %s", self.root, self.src_dir)

        return typing.cast("Path", self.src_dir)


    def _check_exists(self) -> None:
        if not self.root.exists():
            LOGGER.error("Invalid path: %s does not exist.", self.root)
            raise HTTPException(status_code=400, detail="Invalid Path")

        LOGGER.info("Path exists: %s", self.root)

    def _check_is_directory(self) -> None:
        if not self.root.is_dir():
            LOGGER.error("Path is not a directory: %s", self.root)
            raise HTTPException(status_code=400, detail="Path is not a directory")

        LOGGER.info("Path '%s' is valid.", self.root)


    def _check_permissions(self) -> None:
        """Check read.write permissions to the root folder."""
        if not os.access(self.root, os.R_OK):
            LOGGER.error("Folder is not readable: %s", self.root)
            raise PermissionError("Folder '%s' is not readable.", self.root)

        if not os.access(self.root, os.W_OK):
            LOGGER.error("Folder is not writable: %s", self.root)
            raise PermissionError("Folder '%s' is not writable.", self.root)

        LOGGER.info("Folder '%s' has necessary permissions.", self.root)

    def _detect_project_root(self) -> None:
        """
        Method to detect project root.

        Walk the selected folder recursively and find a directory that contains:
            - src/
            - and a build file (pom.xml or build.gradle or settings.gradle)
        """
        LOGGER.info("Scanning for project root in %s", self.root)
        for path in self.root.rglob("*"):
            if not path.is_dir():
                continue

            src_dir = path / "src"
            if not src_dir.exists():
                continue

            # Now check for build files
            build_files = [
                path / "pom.xml",
                path / "build.gradle",
                path / "settings.gradle",
            ]

            if any(b.exists() for b in build_files):
                self.src_dir = path
                print(path)
                LOGGER.info("Detected project root: %s", self.src_dir)
                return

        raise ValueError("Could not detect project root with src/ and build file.")
