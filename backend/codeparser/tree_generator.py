import os

def generate_file_tree(path, max_depth=3):
    tree = "```\n" + build_tree(path, "", 0, max_depth) + "\n```"
    return tree

def build_tree(current_path, prefix="", depth=0, max_depth=3):
    if depth > max_depth:
        return ""

    entries = sorted(os.listdir(current_path))
    tree_output = ""
    entries = [e for e in entries if not e.startswith(".") and e != "__pycache__"]

    for i, entry in enumerate(entries):
        full_path = os.path.join(current_path, entry)
        connector = "├── " if i < len(entries) - 1 else "└── "

        if os.path.isdir(full_path):
            tree_output += f"{prefix}{connector}{entry}/\n"
            extension = "│   " if i < len(entries) - 1 else "    "
            tree_output += build_tree(full_path, prefix + extension, depth + 1, max_depth)
        else:
            tree_output += f"{prefix}{connector}{entry}\n"

    return tree_output
