import os
from git import Repo

from app.config import REPOSITORIES_DIR


def clone_repository(repo_url: str) -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = os.path.join(REPOSITORIES_DIR, repo_name)

    os.makedirs(REPOSITORIES_DIR, exist_ok=True)

    if os.path.exists(repo_path):
        return repo_path

    Repo.clone_from(repo_url, repo_path)

    return repo_path