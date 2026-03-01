import os

def read_file(path=""):
    """
    Reads a text file and returns first portion.
    """

    if not path:
        return "No file path provided."

    if not os.path.exists(path):
        return "File not found."

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read(2000)

        return f"File content:\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"

