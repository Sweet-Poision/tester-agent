from pathlib import Path
from typing import Any

from pydantic import BaseModel


class JavaParameter(BaseModel):
    name : str
    type: str | None = None

class JavaMethod(BaseModel):
    name: str
    return_type: str | None
    parameters : list[JavaParameter] = []

class JavaClass(BaseModel):
    name : str
    extends: str | None = None
    implements: list[str] = []
    dependencies: list[str] = []
    methods: list[JavaMethod] = []


class ParsedFile(BaseModel):
    file_path: Path
    classes: list[JavaClass]

class Project(BaseModel):
    root: Path
    src_path : Path
    build_system: str
    java_files: list[Path] = []
    endpoints : list[str] = []
    parsed_classes: list[ParsedFile] = []
    dependency_graph: dict[str, dict[str, Any]] = {}


