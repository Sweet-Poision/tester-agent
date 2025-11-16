import logging
from pathlib import Path

import javalang

from app.core.models import ParsedFile

LOGGER = logging.getLogger(__name__)

class ASTDependencyAnalyzer:
    """Analyze Java classes using AST to detect dependencies accurately."""

    def __init__(self, parsed_classes: list[ParsedFile]):
        self.parsed_classes = parsed_classes
        self.class_names = self._collect_all_class_names()

    def _collect_all_class_names(self) -> set:
        names = set()
        for parsed_file in self.parsed_classes:
            for cls in parsed_file.classes:
                names.add(cls.name)
        return names

    def analyze_file(self, file_path: Path) -> set:
        try:
            content = file_path.read_text()
        except Exception as e:
            LOGGER.warning("Failed to read %s: %s", file_path, e)
            return set()

        try:
            tree = javalang.parse.parse(content)
        except javalang.parser.JavaSyntaxError as e:
            LOGGER.warning("Syntax error in %s: %s", file_path, e)
            return set()

        used_classes = set()

        # Check fields and method declarations
        for _, node in tree.filter(javalang.tree.TypeDeclaration):
            if hasattr(node, "fields"):
                for field in getattr(node, "fields", []):
                    for decl in field.declarators:
                        type_name = getattr(field.type, "name", None)
                        if type_name and type_name in self.class_names:
                            used_classes.add(type_name)
            if hasattr(node, "methods"):
                for method in getattr(node, "methods", []):
                    # Return type
                    ret_type = getattr(method.return_type, "name", None)
                    if ret_type and ret_type in self.class_names:
                        used_classes.add(ret_type)
                    # Parameters
                    for param in getattr(method, "parameters", []):
                        param_type = getattr(param.type, "name", None)
                        if param_type and param_type in self.class_names:
                            used_classes.add(param_type)

        return used_classes

    def populate_dependencies(self):
        for parsed_file in self.parsed_classes:
            file_path = parsed_file.file_path
            used_classes = self.analyze_file(file_path)

            for cls in parsed_file.classes:
                cls_name = cls.name
                cls.dependencies = [dep for dep in used_classes if dep != cls_name]

        LOGGER.info("AST-level dependencies populated successfully.")
        return self.parsed_classes
