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

def format_docstring(doc):
    """Clean, dedent, and bullet-style format."""
    cleaned = textwrap.dedent(doc).strip()
    lines = cleaned.splitlines()

    # Show only first 8 lines or truncate with ...
    lines = lines[:8] + (["..."] if len(lines) > 8 else [])

    # Indent and format for Markdown
    return "\n".join([f"  {line.strip()}" for line in lines])


# def parse_python_code(path):
#     output = ""

#     for root, _, files in os.walk(path):
#         for file in files:
#             if file.endswith(".py"):
#                 file_path = os.path.join(root, file)
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as f:
#                         tree = ast.parse(f.read())
#                         for node in ast.iter_child_nodes(tree):
#                             if isinstance(node, ast.FunctionDef):
#                                 name = node.name
#                                 args = [arg.arg for arg in node.args.args]
#                                 doc = ast.get_docstring(node)
#                                 output += f"- **{name}({', '.join(args)})**"
#                                 if doc:
#                                     output += f": {doc.strip()}"
#                                 output += "\n"
#                 except Exception as e:
#                     print(f"Error reading {file_path}: {e}")

#     return output.strip()


# def parse_python_code(path): 
#     docs = ""
#     for root, _, files in os.walk(path):
#         for file in files:
#             if file.endswith(".py"):
#                 with open(os.path.join(root, file), "r", encoding="utf-8") as f:
#                     try:
#                         tree = ast.parse(f.read())
#                         for node in ast.walk(tree):
#                             if isinstance(node, ast.FunctionDef):
#                                 docs += f"- {node.name}({', '.join([arg.arg for arg in node.args.args])})\n"
#                     except Exception:
#                         pass
#     return docs
