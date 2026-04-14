import subprocess
import shutil
import os

def clone_repo(repo_url, folder="temp_repo"):
    if os.path.exists(folder):
        shutil.rmtree(folder)

    subprocess.run(["git", "clone", repo_url, folder], check=True)

    return folder


def read_repo_code(folder):
    code = ""

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith((".py", ".cpp", ".js", ".ts", ".java")):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", errors="ignore") as f:
                        code += f.read()[:2000] + "\n\n"
                except:
                    continue

    return code[:8000]