import os

def get_files(path):
    valid_ext = (".py", ".js", ".jsx", ".java", ".ts", ".md", ".cpp", ".c", ".html", ".css")
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(valid_ext):
                files.append(os.path.join(root, f))
    return files
