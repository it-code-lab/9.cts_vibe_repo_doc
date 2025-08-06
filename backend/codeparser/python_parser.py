import os
import ast

import os
import ast
import textwrap

def parse_python_code(path):
    output = ""

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        for node in ast.iter_child_nodes(tree):
                            if isinstance(node, ast.FunctionDef):
                                name = node.name
                                args = [arg.arg for arg in node.args.args]
                                doc = ast.get_docstring(node)
                                output += f"### `{name}({', '.join(args)})`\n"

                                if doc:
                                    lines = textwrap.dedent(doc).strip().splitlines()
                                    if lines:
                                        output += f"**Description:** {lines[0].strip()}\n\n"
                                        if len(lines) > 1:
                                            output += "**Details:**\n"
                                            for line in lines[1:]:
                                                stripped = line.strip().lstrip("-:•* ")
                                                if stripped:
                                                    output += f"- {stripped}\n"
                                output += "\n"

                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    return output.strip()
def extract_routes(path):
    routes = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        line = line.strip()

                        # Match FastAPI or Flask route decorators
                        if line.startswith("@app.") and ("/" in line or "route(" in line):
                            method = None
                            route_path = None

                            # FastAPI: @app.get("/users")
                            if "(" in line:
                                method_part = line.split("(")[0].replace("@app.", "").strip()
                                method = method_part.upper()
                                route_path = line.split("(", 1)[1].split(")")[0].strip("\"'")

                                # Flask fallback if method is inside route()
                                if method == "ROUTE":
                                    methods_line = next((l for l in lines[i:i+5] if "methods=" in l), "")
                                    method_list = extract_methods(methods_line)
                                    method = ", ".join(method_list)

                            if method and route_path:
                                routes.append(f"- **{method}** `{route_path}`")
                except Exception as e:
                    print(f"Error parsing routes in {file_path}: {e}")

    return routes


def extract_methods(line):
    # Extracts methods from Flask-style methods=["GET", "POST"]
    import re
    match = re.search(r'methods\s*=\s*\[([^\]]+)\]', line)
    if match:
        return [m.strip().strip('"\'') for m in match.group(1).split(",")]
    return ["GET"]

def format_docstring(doc):
    """Clean, dedent, and bullet-style format."""
    cleaned = textwrap.dedent(doc).strip()
    lines = cleaned.splitlines()

    # Show only first 8 lines or truncate with ...
    lines = lines[:8] + (["..."] if len(lines) > 8 else [])

    # Indent and format for Markdown
    return "\n".join([f"  {line.strip()}" for line in lines])


