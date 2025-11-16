from pathlib import Path

from pydantic import BaseModel


class JavaMethod(BaseModel):
    name: str

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
    endpoints : list[str]
    parsed_classes: list[ParsedFile] = []
    dependency_graph: dict = {}


