# src/app/core/java_parser.py
import logging
from pathlib import Path

import javalang

from app.core.models import JavaClass, JavaMethod, JavaParameter, ParsedFile

LOGGER = logging.getLogger(__name__)

def _get_type_name(type_node) -> str | None :
    """
    Safely extract a readable type string from a javalang type node.

    For generics it will produce a simple representation like. List<User>
    """
    if not type_node:
        return None

    # Basic types (int, boolean) may have name attributes on node
    name = getattr(type_node, "name", None)
    if not name:
        # Some nodes (like BasicType) might use 'type' or be repr-able
        return str(type_node)

    args = []
    for arg in getattr(type_node, "arguments", []) or []:
        t = getattr(arg, "type", None)
        if t:
            arg_name = getattr(t, "name", None)
            if arg_name:
                args.append(arg_name)

    if args:
        return f"{name}<{','.join(args)}>"
    return name


class JavaParser:
    def __init__(self, java_files: list[Path]):
        self.java_files = java_files

    def parse_all(self) -> list[ParsedFile]:
        parsed_files: list[ParsedFile] = []
        for file_path in self.java_files:
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    source = f.read()
            except Exception as e:
                LOGGER.warning("Failed to read %s: %s", file_path, e)
                continue

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
        except javalang.parser.JavaSyntaxError as e:
            LOGGER.warning("javalang failed to parse file (syntax): %s", e)
            return []
        except Exception as e:
            LOGGER.warning("javalang failed to parse file: %s", e)
            return []

        classes = []
        for _, node in tree.filter(javalang.tree.ClassDeclaration):
            methods = []
            for m in getattr(node, "methods", []) or []:

                ret = None  # return type
                if getattr(m, "return_type", None):
                    ret = _get_type_name(m.return_type)

                # parameters
                params = []
                for p in getattr(m, "parameters", []) or []:
                    p_type = _get_type_name(getattr(p, "type", None))
                    params.append(JavaParameter(name=p.name, type=p_type))

                methods.append(JavaMethod(name=m.name, return_type=ret, parameters=params))

            classes.append(
                JavaClass(
                    name = node.name,
                    extends = node.extends.name if node.extends else None,
                    implements = [i.name for i in node.implements] if node.implements else [],
                    dependencies = [],  # optional: can extract from fields/methods
                    methods = methods,
                ),
            )
        return classes
