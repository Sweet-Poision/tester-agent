import logging
from pathlib import Path

import javalang

from app.core.models import ParsedFile

LOGGER = logging.getLogger(__name__)

class ASTDependencyAnalyzer:
    """Analyze Java classes using AST to detect dependencies accurately."""

    def __init__(self, parsed_files: list[ParsedFile]):
        self.parsed_files = parsed_files
        self.class_names = self._collect_all_class_names()

    def _collect_all_class_names(self) -> set:
        names = set()
        for parsed_file in self.parsed_files:
            for cls in parsed_file.classes:
                names.add(cls.name)
        return names

    def analyze_file(self, file_path: Path) -> set:
        """Use both parsed signatures (fast) and AST fallback (fields / complex types) to discover used classes within the project."""
        used = set()

        # 1) Fast path: find parsed file and use its method signatures
        pf = next((pf for pf in self.parsed_files if pf.file_path == file_path), None)

        if pf:
            for cls in pf.classes:
            # method return types / parameter types
                for m in cls.methods:
                    if m.return_type and m.return_type in self.class_names:
                        used.add(m.return_type)
                    for p in m.parameters:
                        if p.type and p.type in self.class_names:
                            used.add(p.type)

        # 2) AST fallback for fields and types referenced in code
        try:
            content = file_path.read_text()
        except Exception as e:
            LOGGER.warning("Failed to read %s: %s", file_path, e)
            return used

        try:
            tree = javalang.parse.parse(content)
        except javalang.parser.JavaSyntaxError as e:
            LOGGER.debug("Syntax error in %s: %s", file_path, e)
            return used
        except Exception as e:
            LOGGER.warning("AST parse failed for %s: %s", file_path, e)
            return used

        # Check fields and method declarations
        for _, node in tree.filter(javalang.tree.TypeDeclaration):
            # fields
            for field in getattr(node, "fields", []) or []:
                type_name = getattr(field.type, "name", None)
                if type_name and type_name in self.class_names:
                    used.add(type_name)

            # methods (fallback) - covers some edge cases not captured earlier
            for method in getattr(node, "methods", []) or []:
                ret_type = getattr(method, "return_type", None)
                if ret_type:
                    rt = getattr(ret_type, "name", None)
                    if rt and rt in self.class_names:
                        used.add(rt)
                for param in getattr(method, "parameters", []) or []:
                    pt = getattr(getattr(param, "type", None), "name", None)
                    if pt and pt in self.class_names:
                        used.add(pt)

        return used

    def populate_dependencies(self) -> list[ParsedFile]:
        for parsed_file in self.parsed_files:
            file_path = parsed_file.file_path
            used_classes = self.analyze_file(file_path)

            for cls in parsed_file.classes:
                # cls_name = cls.name
                cls.dependencies = [dep for dep in sorted(used_classes) if dep != cls.name]

        LOGGER.info("AST-level dependencies populated successfully.")
        return self.parsed_files
