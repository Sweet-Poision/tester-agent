import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)

EXCLUDED_DIRS = {
    "src/test",
    "build",
    "target",
    ".gradle",
    "node_modeuls",
}

class JavaScanner:
    def __init__(self, project_root: Path):
        self._project_root : Path = project_root
        self._src_root = project_root / "src" / "main" / "java"

    def discover_java_files(self) -> list[Path]:
        """
        Return a list of all Java source files under src/main/java.

        It excludes files which are irrlevant build/test directories.
        """
        java_files = []

        for path in self._src_root.rglob("*.java"):
            # check if any excluded dir is in the path
            if any(excluded in str(path) for excluded in EXCLUDED_DIRS):
                LOGGER.info("Excluding file from scan: %s", path)
                continue

            java_files.append(path)

        LOGGER.info("Discovered %d Java source files", len(java_files))
        return java_files


