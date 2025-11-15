import subprocess
import json
import os

OLLAMA_PATH = "ollama"

def local_llm(prompt, model_name="phi"):
    """
    Runs a local LLM using Ollama, with CPU-safe fallback.
    """
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        return result.stdout.strip() or "⚠️ No output received from model."
    except subprocess.CalledProcessError as e:
        return f"⚠️ Ollama Error: {e.stderr or e}"
    except FileNotFoundError:
        return "⚠️ Ollama not found. Please check OLLAMA_PATH."
    except Exception as e:
        return f"⚠️ LLM Error: {str(e)}"


def summarize_file(file_path, model_name):
    """
    Summarizes a single file using Ollama locally.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        prompt = f"Summarize what this file does:\n\n{content[:4000]}"

        result = subprocess.run(
            [OLLAMA_PATH, "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        return result.stdout.strip() or "⚠️ No output received from model."
    except subprocess.CalledProcessError as e:
        return f"⚠️ LLM Error (Ollama failed): {e.stderr or e}"
    except Exception as e:
        return f"⚠️ LLM Error: {e}"


def summarize_overall(file_summaries, model_name):
    """
    Generates a high-level summary of the entire repository.
    """
    try:
        summaries_text = json.dumps(file_summaries, indent=2, ensure_ascii=False)
        prompt = (
            "Given the following file summaries, explain the overall purpose, "
            "architecture, and main functionality of this project in detail:\n\n"
            f"{summaries_text[:4000]}\n\nProject Summary:"
        )
        return local_llm(prompt, model_name)
    except Exception as e:
        return f"⚠️ LLM Error: {e}"
