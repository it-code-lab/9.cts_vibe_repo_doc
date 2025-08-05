import os

def extract_env_vars(path):
    env_vars = set()

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") or file == ".env":
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if "os.getenv(" in line or "os.environ.get(" in line:
                            var = extract_var_from_line(line)
                            if var:
                                env_vars.add(var)
                        elif "=" in line and not line.startswith("#") and file == ".env":
                            env_vars.add(line.split("=")[0].strip())

    return sorted(env_vars)

def extract_var_from_line(line):
    import re
    match = re.search(r'os\.(?:getenv|environ\.get)\(["\'](.+?)["\']', line)
    return match.group(1) if match else None

def generate_env_sample(env_vars):
    return "\n".join([f"{var}=" for var in env_vars])


# import os

# def extract_env_vars(path):
#     env_lines = []
#     for root, _, files in os.walk(path):
#         for file in files:
#             if file == ".env":
#                 with open(os.path.join(root, file), "r") as f:
#                     for line in f:
#                         if "=" in line:
#                             env_lines.append(line.strip())
#     return "\n".join(env_lines)
