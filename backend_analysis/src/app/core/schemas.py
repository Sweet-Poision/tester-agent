from pydantic import BaseModel


class PathRequest(BaseModel):
    path: str

class ProjectResponse(BaseModel):
    project_id: str
    status: str
    build_system: str
