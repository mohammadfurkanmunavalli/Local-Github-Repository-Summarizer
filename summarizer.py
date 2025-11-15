import os
import shutil
import stat
from git import Repo
from utils.repo_utils import get_files
from utils.llm_utils import summarize_file, summarize_overall


def on_rm_error(func, path, exc_info):
    """Force-remove read-only files or locked git pack files on Windows."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"⚠️ Could not delete {path}: {e}")


def analyze_repo(repo_url, model_name):
    repo_dir = "repo_clone"

    # ✅ If local folder, use directly
    if os.path.isdir(repo_url):
        repo_dir = repo_url
    else:
        # ✅ If old repo exists, remove it safely
        if os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir, onerror=on_rm_error)
            except Exception as e:
                print(f"⚠️ Could not delete {repo_dir}: {e}")
                return {"error": f"Failed to remove old directory: {e}"}

        # ✅ Clone repository fresh
        try:
            Repo.clone_from(repo_url, repo_dir)
        except Exception as e:
            print(f"❌ Error cloning repo: {e}")
            return {"error": f"Failed to clone repository: {e}"}

    # ✅ Get files and summarize
    try:
        files = get_files(repo_dir)
    except Exception as e:
        return {"error": f"Error reading repository files: {e}"}

    summaries = {}
    for f in files:
        try:
            summaries[f] = summarize_file(f, model_name)
        except Exception as e:
            summaries[f] = f"⚠️ Error summarizing {f}: {e}"

    try:
        overall_summary = summarize_overall(summaries, model_name)
    except Exception as e:
        overall_summary = f"⚠️ Error generating overall summary: {e}"

    # ✅ Markdown output
    markdown_output = "# Repository Summary\n\n"
    for file, summary in summaries.items():
        markdown_output += f"## {file}\n{summary}\n\n"
    markdown_output += f"## Overall Summary\n{overall_summary}"

    return {
        "files": summaries,
        "overall_summary": overall_summary,
        "markdown": markdown_output
    }
