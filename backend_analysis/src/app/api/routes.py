from fastapi import APIRouter, HTTPException

from app.core.project_registry import _registry, get, store
from app.core.project_service import project_service
from app.core.schemas import PathRequest, ProjectResponse

router = APIRouter()

@router.post("/start-analysis")
async def start_analysis(req: PathRequest):
    try:
        project = project_service.initialize(req.path)
        project_id = store(project)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return ProjectResponse(
            project_id = project_id,
            status = "initialized",
            build_system = project.build_system,
        )


@router.get("/projects")
async def get_all_projects():
    all_projects = _registry
    result = {}
    for pid, project in all_projects.items():
        result[pid] = {
            "root" : str(project.root),
            "build_system" : project.build_system,
            "java_files_count" : len(project.java_files),
        }
    return result


@router.get("/endpoints/{project_id}")
async def get_endpoints(project_id: str):
    project = get(project_id)
    if not project:
        return {"error" : "Project not found"}
    return project.endpoints

@router.get("/projects/{project_id}/parsed_classes")
async def get_parsed_classes(project_id: str):
    project = get(project_id)
    if not project:
        return {"error": "Project not found"}

    result = []
    for parsed_file in project.parsed_classes:
        result.append({
            "file_path" : str(parsed_file.file_path),
            "classes" : [cls.model_dump() for cls in parsed_file.classes],
        })
    return result
