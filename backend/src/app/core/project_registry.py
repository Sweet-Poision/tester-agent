import uuid

_registry = {}

def store(project) -> str:
    """Store a Project object and return a unique project id."""
    project_id = str(uuid.uuid4())
    _registry[project_id] = project
    return project_id


def get(project_id):
    """Retrieve a Project object by project_id."""
    return _registry.get(project_id)
