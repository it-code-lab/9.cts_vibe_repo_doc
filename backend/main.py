from fastapi import FastAPI, UploadFile, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from codeparser.python_parser import parse_python_code, extract_routes
from codeparser.env_parser import extract_env_vars, generate_env_sample
from utils.repo_handler import handle_uploaded_zip, handle_repo_clone
from codeparser.overview_generator import generate_project_overview
from codeparser.tree_generator import generate_file_tree
from fastapi.responses import FileResponse
from utils.doc_bundler import bundle_docs

import shutil
import os

app = FastAPI()

# CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
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

        routes = extract_routes(project_path)
        parsed_data = parse_python_code(project_path)
        env_vars = extract_env_vars(project_path)
        env_sample = generate_env_sample(env_vars)
        overview = generate_project_overview(project_path)
        file_tree = generate_file_tree(project_path)

        # Format the README
        readme_content = f"# Auto-Generated README\n\n{overview}\n"

        readme_content += f"## File Tree:\n{file_tree}\n"

        if parsed_data:
            readme_content += f"## Functions:\n{parsed_data}\n\n"

        if routes:
            readme_content += f"## API Routes:\n" + "\n".join(routes) + "\n\n"

        if env_sample:
            readme_content += f"## .env variables:\n{env_sample}\n"

        return {
            "readme": readme_content,
            "env_sample": env_sample
        }
    except HTTPException as he:
        raise he  # let FastAPI handle it
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/analyze/")
# async def analyze_code(file: UploadFile):
#     project_path = await handle_uploaded_zip(file)
#     parsed_data = parse_python_code(project_path)
#     env_vars = extract_env_vars(project_path)
    
#     # Combine into simple README for now
#     readme_content = f"# Auto-Generated README\n\n## Functions:\n{parsed_data}\n\n## .env variables:\n{env_vars}"
#     with open(os.path.join(project_path, "README.md"), "w") as f:
#         f.write(readme_content)

#     return {"readme": readme_content}


@app.get("/")
def root():
    return {"status": "Backend is working"}

@app.post("/download-docs/")
async def download_docs(file: UploadFile = None, repo_url: str = Form(None)):
    try:
        if file:
            project_path = await handle_uploaded_zip(file)
        elif repo_url:
            project_path = handle_repo_clone(repo_url)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        routes = extract_routes(project_path)
        functions = parse_python_code(project_path)
        env_vars = extract_env_vars(project_path)
        env_sample = generate_env_sample(env_vars)
        overview = generate_project_overview(project_path)
        file_tree = generate_file_tree(project_path)

        # Assemble readme
        readme_content = f"# Auto-Generated README\n\n{overview}\n"
        readme_content += f"## File Tree:\n{file_tree}\n\n"
        if functions:
            readme_content += f"## Functions:\n{functions}\n\n"
        if routes:
            readme_content += f"## API Routes:\n" + "\n".join(routes) + "\n\n"
        if env_sample:
            readme_content += f"## .env variables:\n{env_sample}\n"

        # Bundle
        zip_path = bundle_docs(readme_content, env_sample if env_sample else None)
        return FileResponse(zip_path, filename="project_docs.zip", media_type="application/zip")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
