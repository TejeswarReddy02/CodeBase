from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repository.loader import clone_repository


router = APIRouter(
    prefix="/repository",
    tags=["Repository"]
)


class RepositoryRequest(BaseModel):
    repo_url: str


@router.post("/clone")
def clone_repo(request: RepositoryRequest):

    try:
        repo_path = clone_repository(request.repo_url)

        return {
            "message": "Repository cloned successfully",
            "repository_path": repo_path
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )