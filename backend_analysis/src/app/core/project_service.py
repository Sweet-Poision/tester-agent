from app.core.ast_dependency_analyzer import ASTDependencyAnalyzer
from app.core.dependency_graph import DependencyGraphBuilder
from app.core.java_parser import JavaParser
from app.core.models import Project
from app.core.project_scanner import JavaScanner
from app.utils.path_utils import PathUtils


class ProjectService:
    """Service to handle project initialization and management."""

    def initialize(self, folder_path: str) -> Project:
        # validate and detect project root
        path_utils = PathUtils(folder_path)
        project_root = path_utils.validate_project_structure()

        src_path = project_root / "src"
        # finding the java build system
        build_system = "maven" if (project_root / "pom.xml").exists() else "gradle"

        project = Project(
            root=project_root,
            src_path = src_path,
            build_system = build_system,
            endpoints = [],
        )

        # discovering java files
        java_scanner = JavaScanner(project_root)
        project.java_files = java_scanner.discover_java_files()

        # parsing java files
        parser = JavaParser(project.java_files)
        project.parsed_classes = parser.parse_all()

        # populating dependencies using AST
        analyzer = ASTDependencyAnalyzer(parsed_files=project.parsed_classes)
        analyzer.populate_dependencies()

        # build dependency graph
        graph_builder = DependencyGraphBuilder(project.parsed_classes)
        project.dependency_graph = graph_builder.build()

        return project


project_service = ProjectService()
