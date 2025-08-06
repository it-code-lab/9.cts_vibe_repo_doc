import os, shutil, zipfile, tempfile
import tempfile
import git
from fastapi import HTTPException

async def handle_uploaded_zip(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, uploaded_file.filename)

    with open(zip_path, "wb") as f:
        f.write(await uploaded_file.read())

    extract_path = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path



def handle_repo_clone(url):
    temp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(url, temp_dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {str(e)}")
    return temp_dir