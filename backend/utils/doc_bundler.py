import os
import zipfile
import tempfile

def bundle_docs(readme_text, env_sample_text=None):
    temp_dir = tempfile.mkdtemp()

    readme_path = os.path.join(temp_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text)

    if env_sample_text:
        env_path = os.path.join(temp_dir, ".env.sample")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_sample_text)

    zip_path = os.path.join(temp_dir, "project_docs.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(readme_path, "README.md")
        if env_sample_text:
            zipf.write(env_path, ".env.sample")

    return zip_path
