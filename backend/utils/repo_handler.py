import os, shutil, zipfile, tempfile
import tempfile
import git
from fastapi import HTTPException

async def handle_uploaded_zip(file):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, file.filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir


def handle_repo_clone(url):
    temp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(url, temp_dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {str(e)}")
    return temp_dir