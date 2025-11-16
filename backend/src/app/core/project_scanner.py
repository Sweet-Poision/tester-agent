import logging
from pathlib import Path

EXCLUDED_DIRS = {
    "target", "build", "out", ".gradle", ".mvn", "__pycache__", "node_modules", "test", "tests",
}

LOGGER = logging.getLogger(__name__)

class ProjectScanner:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()


    def scan_java_files(self) -> list[dict]:
        """Recursively scan for .java files."""
        files = []

        for path in self.root.rglob("*.java"):
            # exclude folders like target, build, out, .gradle, .mvn, __pycache__, node_modules, test, tests
            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue

            files.append({
                "path": str(path),
                "relative_path": str(path.relative_to(self.root)),
                "filename": path.name,
            })

            if(not files):
                LOGGER.info("No Java files found in the project.")
                raise FileNotFoundError("No Java files found in the project.")

            LOGGER.info("Found %d Java Files.", len(files))

        return files

    def create_tests_folder(self) -> Path:
        """Create /tests folder if it doesn't exist inside project."""
        # We will check in future where to create tests folder
        tests_folder = self.root / "tests"

        tests_folder.mkdir(parents=True, exist_ok=True)
        LOGGER.info("Tests folder ensured at: %s", str(tests_folder))
        return tests_folder
