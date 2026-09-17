import os


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".cs": "csharp",
    ".swift": "swift",
    ".kt": "kotlin",
}


def read_repository(repository_path: str) -> list[dict]:

    files = []

    for root, directories, filenames in os.walk(repository_path):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in filenames:

            extension = os.path.splitext(filename)[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(
                root,
                filename
            )

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    content = file.read()

            except (UnicodeDecodeError, OSError):

                continue

            relative_path = os.path.relpath(
                file_path,
                repository_path
            )

            files.append(
                {
                    "file_path": relative_path,
                    "language": SUPPORTED_EXTENSIONS[extension],
                    "content": content,
                    "line_count": len(content.splitlines())
                }
            )

    return files