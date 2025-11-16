import logging

from app.core.models import ParsedFile

LOGGER = logging.getLogger(__name__)

class DependencyGraphBuilder:
    """
    Builds a dependency graph from parsed Java classes.
    
    Stores class relationships and provides methods to query and update graph.
    """

    def __init__(self, parsed_classes: list[ParsedFile]):
        """
        Constructor.

        Args:
            parsed_classes: {file_path: [class_info_dicts]}

        """
        self.parsed_classes = parsed_classes
        self.graph: dict[str, dict] = {}

    def build(self) -> dict[str, dict]:
        """Construct the dependency graph."""
        for parsed_file in self.parsed_classes:
            file_path = parsed_file.file_path

            for cls in parsed_file.classes:
                class_name = cls.name
                self.graph[class_name] = {
                    "file_path" : file_path,
                    "extends" : cls.extends,
                    "implements" : cls.implements,
                    "dependencies" : cls.dependencies,
                    "methods": [method.name for method in cls.methods],
                }
        LOGGER.info("Dependency graph build with %d classes", len(self.graph))
        return self.graph

    def add_dependency(self, class_name: str, dependency: str) -> None:
        """Add a dependency to a class in the graph."""
        if class_name in self.graph:
            deps = self.graph[class_name].setdefault("dependencies", [])
            if dependency not in deps:
                deps.append(dependency)
                LOGGER.debug("Added dependency '%s' to class '%s'", dependency, class_name)


    def get_class_info(self, class_name: str) -> None | dict:
        """Return information about a class."""
        return self.graph.get(class_name)

    def list_classes(self) -> list[str]:
        """Return all class names in the graph."""
        return list(self.graph.keys())
