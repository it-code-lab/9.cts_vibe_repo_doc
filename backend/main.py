from fastapi import FastAPI, UploadFile, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from codeparser.python_parser import parse_python_code, extract_routes
from codeparser.env_parser import extract_env_vars, generate_env_sample
from codeparser.java_parser import parse_java_code
from codeparser.overview_generator import generate_project_overview
from codeparser.tree_generator import generate_file_tree

from utils.repo_handler import handle_uploaded_zip, handle_repo_clone
from utils.doc_bundler import bundle_docs
from fastapi.staticfiles import StaticFiles

import os
import re

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze/")
async def analyze_code(request: Request, file: UploadFile = None, repo_url: str = Form(None)):
    GITHUB_REPO_REGEX = r'^https:\/\/github\.com\/[^\/]+\/[^\/]+$'

    try:
        if file:
            project_path = await handle_uploaded_zip(file)
        elif repo_url:
            if not re.match(GITHUB_REPO_REGEX, repo_url.strip()):
                raise HTTPException(status_code=400, detail="Invalid GitHub repository URL.")
            project_path = handle_repo_clone(repo_url)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        # --- Core Analysis ---
        routes = extract_routes(project_path)
        env_vars = extract_env_vars(project_path)
        env_sample = generate_env_sample(env_vars)
        overview = generate_project_overview(project_path)
        file_tree = generate_file_tree(project_path)

        # --- Language-specific Parsing ---
        python_output = parse_python_code(project_path)
        java_output = parse_java_code(project_path)

        # --- Generate README Content ---
        readme_content = f"# Auto-Generated README\n\n{overview}\n"
        readme_content += f"## File Tree:\n{file_tree}\n"

        if python_output:
            readme_content += "## Python Functions:\n"
            readme_content += f"{python_output}\n\n"

        if isinstance(java_output, dict) and (java_output.get("classes") or java_output.get("methods")):
            readme_content += "## Java Classes & Methods:\n"
            for cls in java_output.get("classes", []):
                readme_content += f"### Class: `{cls['name']}`\n"
                if cls["doc"]:
                    readme_content += f"{cls['doc']}\n\n"

            for method in java_output.get("methods", []):
                readme_content += f"- Method: `{method['name']}({method['args']})`\n"
                if method["doc"]:
                    readme_content += f"  {method['doc']}\n"

        if routes:
            readme_content += f"\n## API Routes:\n" + "\n".join(routes) + "\n"

        if env_sample:
            readme_content += f"\n## .env variables:\n{env_sample}\n"

        return {
            "readme": readme_content,
            "env_sample": env_sample
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download-docs/")
async def download_docs(file: UploadFile = None, repo_url: str = Form(None)):
    try:
        if file:
            project_path = await handle_uploaded_zip(file)
        elif repo_url:
            project_path = handle_repo_clone(repo_url)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        # --- Core Analysis ---
        routes = extract_routes(project_path)
        env_vars = extract_env_vars(project_path)
        env_sample = generate_env_sample(env_vars)
        overview = generate_project_overview(project_path)
        file_tree = generate_file_tree(project_path)

        # --- Language-specific Parsing ---
        python_output = parse_python_code(project_path)
        java_output = parse_java_code(project_path)

        # --- Generate README Content ---
        readme_content = f"# Auto-Generated README\n\n{overview}\n"
        readme_content += f"## File Tree:\n{file_tree}\n"

        if python_output:
            readme_content += "## Python Functions:\n"
            readme_content += f"{python_output}\n\n"

        if isinstance(java_output, dict) and (java_output.get("classes") or java_output.get("methods")):
            readme_content += "## Java Classes & Methods:\n"
            for cls in java_output.get("classes", []):
                readme_content += f"### Class: `{cls['name']}`\n"
                if cls["doc"]:
                    readme_content += f"{cls['doc']}\n\n"

            for method in java_output.get("methods", []):
                readme_content += f"- Method: `{method['name']}({method['args']})`\n"
                if method["doc"]:
                    readme_content += f"  {method['doc']}\n"

        if routes:
            readme_content += f"\n## API Routes:\n" + "\n".join(routes) + "\n"

        if env_sample:
            readme_content += f"\n## .env variables:\n{env_sample}\n"

        # Bundle and send ZIP
        zip_path = bundle_docs(readme_content, env_sample if env_sample else None)
        return FileResponse(zip_path, filename="project_docs.zip", media_type="application/zip")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/")
# def root():
#     return {"status": "Backend is working"}

# Health endpoint (optional)
@app.get("/health")
def health():
    return {"ok": True}

# Serve React build (placed in backend/static)
app.mount("/", StaticFiles(directory="static", html=True), name="static")