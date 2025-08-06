import re
from pathlib import Path
import os

def parse_java_code(project_path):
    all_classes = []
    all_methods = []

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")

                    class_pattern = r'(?:/\*\*[\s\S]*?\*/)?\s*public\s+class\s+(\w+)'
                    method_pattern = r'(?:/\*\*[\s\S]*?\*/)?\s*public\s+[^\s]+\s+(\w+)\s*\((.*?)\)'

                    for class_match in re.finditer(class_pattern, content):
                        javadoc = extract_javadoc_before(content, class_match.start())
                        class_name = class_match.group(1)
                        all_classes.append({
                            "name": class_name,
                            "doc": javadoc.strip()
                        })

                    for method_match in re.finditer(method_pattern, content):
                        javadoc = extract_javadoc_before(content, method_match.start())
                        method_name = method_match.group(1)
                        args = method_match.group(2)
                        all_methods.append({
                            "name": method_name,
                            "args": args,
                            "doc": javadoc.strip()
                        })
                except Exception as e:
                    # You might want to log this or handle it differently
                    print(f"Error parsing Java file {file_path}: {e}")

    return {
        "classes": all_classes,
        "methods": all_methods
    }

def extract_javadoc_before(content, index):
    before = content[:index]
    matches = list(re.finditer(r'/\*\*[\s\S]*?\*/', before))
    return matches[-1].group(0) if matches else ""