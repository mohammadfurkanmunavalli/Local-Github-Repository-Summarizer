import os
import tempfile
import zipfile
import shutil
from git import Repo, GitCommandError
from pathlib import Path
from typing import List

def clone_repo(url: str, dest_root: str) -> str:
    """
    Clone the repo into dest_root/<repo_name> and return path.
    """
    try:
        Path(dest_root).mkdir(parents=True, exist_ok=True)
        repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
        dest = os.path.join(dest_root, repo_name)
        
        if os.path.exists(dest):
            # If repo exists, pull latest
            try:
                repo = Repo(dest)
                repo.remotes.origin.pull()
                return dest
            except Exception:
                shutil.rmtree(dest)
        
        print(f"Cloning repository: {url}")
        Repo.clone_from(url, dest)
        return dest
    except GitCommandError as e:
        if "Repository not found" in str(e):
            raise ValueError(f"Repository not found: {url}. Please check if the repository exists and is public.")
        else:
            raise e

def extract_zip(uploaded_file, dest_root: str) -> str:
    """
    uploaded_file should be a file-like object (from Streamlit upload) or path
    Extracts zip to a temporary folder and returns the path.
    """
    dest = os.path.join(dest_root, "uploaded_repo")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(uploaded_file, "r") as z:
        z.extractall(dest)
    return dest

def list_code_files(repo_path: str, exts=None) -> List[str]:
    """
    Walk repo_path and return list of file paths with code extensions
    """
    if exts is None:
        exts = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".md", ".json", ".yml", ".yaml", ".rs", ".go", ".html", ".css", ".txt"}
    files = []
    for root, _, filenames in os.walk(repo_path):
        # skip .git and other hidden directories
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
        for f in filenames:
            if Path(f).suffix.lower() in exts:
                files.append(os.path.join(root, f))
    # sort by size (small to large) or keep natural
    files.sort(key=lambda p: os.path.getsize(p))
    return files

def read_file(path: str, max_chars=20000) -> str:
    """
    Read a file with safe fallback and limit size.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            if len(text) > max_chars:
                return text[:max_chars] + "\n\n... (truncated)"
            return text
    except Exception as e:
        return f"Could not read file: {e}"