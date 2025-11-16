# src/app/core/java_parser.py
from pathlib import Path

import javalang

from app.core.models import JavaClass, JavaMethod, ParsedFile


class JavaParser:
    def __init__(self, java_files: list[Path]):
        self.java_files = java_files

    def parse_all(self) -> list[ParsedFile]:
        parsed_files: list[ParsedFile] = []
        for file_path in self.java_files:
            with file_path.open("r", encoding="utf-8") as f:
                source = f.read()
            parsed_files.append(
                ParsedFile(
                    file_path=file_path,
                    classes=self._parse_file(source),
                ),
            )
        return parsed_files

    def _parse_file(self, source: str) -> list[JavaClass]:
        try:
            tree = javalang.parse.parse(source)
        except javalang.parser.JavaSyntaxError:
            return []

        classes = []
        for _, node in tree.filter(javalang.tree.ClassDeclaration):
            classes.append(
                JavaClass(
                    name = node.name,
                    extends = node.extends.name if node.extends else None,
                    implements = [i.name for i in node.implements] if node.implements else [],
                    dependencies = [],  # optional: can extract from fields/methods
                    methods = [JavaMethod(name=m.name) for m in node.methods],
                ),
            )
        return classes
