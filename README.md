# Java Project Analyzer – Backend

A backend service that scans a Java project, parses source files, builds dependency graphs, and prepares structured context for automated test-case generation using an LLM server.

This repository contains **the project-analysis backend only**. A separate LLM service will be added next.

---

## Purpose
The system analyzes Java codebases to extract:
- Directory structure
- Java classes
- Extended/implemented classes and interfaces
- Methods inside each class
- Return types
- Method parameters
- AST-based dependency relationships

This structured model will later be fed into an external LLM service to generate intelligent test cases.

---

## Current Features (Completed)
### 1. **Project Structure Detection**
- Automatically detects the project root.
- Supports Maven and Gradle.
- Correctly identifies `src/main/java` even if the scanned folder itself *is* the `src` folder.

### 2. **Java File Discovery**
- Recursively scans all Java source folders.
- Produces a clean list of all `.java` files.

### 3. **Java Parsing Using `javalang`**
Extracts:
- Class name
- Parent class (extends)
- Implemented interfaces
- Method names
- Method return types
- Method parameters (name + type)
- Custom object types

Everything is mapped into Pydantic models for type safety.

### 4. **AST-Based Dependency Graph**
- Cross-file dependency resolution
- Method → class references
- Class → class references
- Compatible with future AI usage

### 5. **Clean Service Architecture**
Core services include:
- `ProjectService`
- `JavaScanner`
- `JavaParser`
- `ASTDependencyAnalyzer`
- `DependencyGraphBuilder`
- `PathUtils`

Everything is modular, production-ready, and extendable.

---

## Upcoming Work (Next Steps)
### 1. **Separate LLM Server**
A second server will be added:
- Handles large prompts
- Runs async
- Accepts structured analysis data
- Generates test cases
- Keeps backend responsive

### 2. **Test-Case Generator API**
- Accepts project model
- Generates JUnit test files
- Handles mocks, stubs, and custom object instantiation automatically

### 3. **Improved Type Resolution**
- Full import-based type linking
- Intelligent detection of custom classes vs Java builtin classes

### 4. **Caching Layer**
- Caches large project scans
- Faster subsequent requests for the same project
### 5. **Performance Hardening**
- Add async tasks
- Prevent blocking in main FastAPI server
---
## Project Structure (Backend Only)
```
src/
  app/
    core/
      project_scanner.py
      java_parser.py
      ast_dependency_analyzer.py
      dependency_graph.py
      models.py
    utils/
      path_utils.py
    services/
      project_service.py
  main.py
README.md
```

---

## Requirements
- Python 3.10+
- FastAPI
- javalang
- Pydantic v2
- Uvicorn
- UV for Python
This backend uses **uv** and **pyproject.toml**, not requirements.txt.

Install dependencies:
```bash
uv sync
```

---
## Running the Server
```bash
uvicorn app.main:app --reload
```

---

## Notes
- The LLM server will **not** run inside this backend.
- All parsed custom objects *will* be correctly represented in the structured context.
- The backend is designed to be production-safe.

---

## Future Vision
Once both servers are ready, the system will:
1. Analyze any Java repo.
2. Build accurate dependency maps.
3. Feed data to LLM server.
4. Auto-generate full test suites.
5. Offer a clean API for CI/CD pipelines.

A complete autonomous Java test-generation engine.

---

## Author
Utsav Raj
