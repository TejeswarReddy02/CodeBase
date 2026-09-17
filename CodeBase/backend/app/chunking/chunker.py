def create_chunks(
    source_code: str,
    file_path: str,
    language: str,
    structure: dict
) -> list[dict]:

    lines = source_code.splitlines()

    chunks = []

    # --------------------------------------------------
    # Helper: create embedding text
    # --------------------------------------------------

    def build_embedding_text(
        chunk_type: str,
        name: str | None,
        start_line: int,
        end_line: int,
        content: str
    ) -> str:

        text = (
            f"File: {file_path}\n"
            f"Language: {language}\n"
            f"Chunk Type: {chunk_type}\n"
        )

        if name:
            text += f"Name: {name}\n"

        text += (
            f"Lines: {start_line}-{end_line}\n\n"
            f"Code:\n"
            f"{content}"
        )

        return text

    # --------------------------------------------------
    # Structural ranges
    # --------------------------------------------------

    structural_ranges = []

    for function in structure["functions"]:

        structural_ranges.append(
            {
                "start": function["start_line"],
                "end": function["end_line"]
            }
        )

    for class_data in structure["classes"]:

        structural_ranges.append(
            {
                "start": class_data["start_line"],
                "end": class_data["end_line"]
            }
        )

    # --------------------------------------------------
    # Function chunks
    # --------------------------------------------------

    for function in structure["functions"]:

        start = function["start_line"] - 1
        end = function["end_line"]

        content = "\n".join(
            lines[start:end]
        )

        chunks.append(
            {
                "chunk_id": (
                    f"{file_path}:"
                    f"function:"
                    f"{function['name']}"
                ),
                "file_path": file_path,
                "language": language,
                "chunk_type": "function",
                "name": function["name"],
                "start_line": function["start_line"],
                "end_line": function["end_line"],
                "content": content,
                "embedding_text": build_embedding_text(
                    "function",
                    function["name"],
                    function["start_line"],
                    function["end_line"],
                    content
                )
            }
        )

    # --------------------------------------------------
    # Class chunks
    # --------------------------------------------------

    for class_data in structure["classes"]:

        start = class_data["start_line"] - 1
        end = class_data["end_line"]

        content = "\n".join(
            lines[start:end]
        )

        chunks.append(
            {
                "chunk_id": (
                    f"{file_path}:"
                    f"class:"
                    f"{class_data['name']}"
                ),
                "file_path": file_path,
                "language": language,
                "chunk_type": "class",
                "name": class_data["name"],
                "start_line": class_data["start_line"],
                "end_line": class_data["end_line"],
                "content": content,
                "embedding_text": build_embedding_text(
                    "class",
                    class_data["name"],
                    class_data["start_line"],
                    class_data["end_line"],
                    content
                )
            }
        )

    # --------------------------------------------------
    # Method chunks
    # --------------------------------------------------

    for method in structure["methods"]:

        start = method["start_line"] - 1
        end = method["end_line"]

        content = "\n".join(
            lines[start:end]
        )

        chunks.append(
            {
                "chunk_id": (
                    f"{file_path}:"
                    f"method:"
                    f"{method['class_name']}."
                    f"{method['name']}"
                ),
                "file_path": file_path,
                "language": language,
                "chunk_type": "method",
                "name": method["name"],
                "class_name": method["class_name"],
                "start_line": method["start_line"],
                "end_line": method["end_line"],
                "content": content,
                "embedding_text": build_embedding_text(
                    "method",
                    f"{method['class_name']}."
                    f"{method['name']}",
                    method["start_line"],
                    method["end_line"],
                    content
                )
            }
        )

    # --------------------------------------------------
    # Module-level chunks
    # --------------------------------------------------

    module_start = None
    module_end = None

    def flush_module_chunk():

        nonlocal module_start
        nonlocal module_end

        if module_start is None:
            return

        content = "\n".join(
            lines[module_start - 1:module_end]
        )

        if content.strip():

            chunks.append(
                {
                    "chunk_id": (
                        f"{file_path}:"
                        f"module:"
                        f"{module_start}-"
                        f"{module_end}"
                    ),
                    "file_path": file_path,
                    "language": language,
                    "chunk_type": "module",
                    "name": None,
                    "start_line": module_start,
                    "end_line": module_end,
                    "content": content,
                    "embedding_text": build_embedding_text(
                        "module",
                        None,
                        module_start,
                        module_end,
                        content
                    )
                }
            )

        module_start = None
        module_end = None

    # --------------------------------------------------
    # Walk through source lines
    # --------------------------------------------------

    for line_number in range(1, len(lines) + 1):

        inside_structure = any(
            item["start"] <= line_number <= item["end"]
            for item in structural_ranges
        )

        if inside_structure:

            flush_module_chunk()

            continue

        line = lines[line_number - 1]

        # Blank lines are allowed inside a module chunk,
        # but leading/trailing blank regions are ignored.
        if module_start is None:

            if not line.strip():
                continue

            module_start = line_number

        module_end = line_number

    flush_module_chunk()

    # --------------------------------------------------
    # Sort chunks by source position
    # --------------------------------------------------

    chunks.sort(
        key=lambda chunk: chunk["start_line"]
    )

    return chunks


def attach_dependencies(
    chunks: list[dict],
    dependencies: list[dict]
) -> list[dict]:

    for chunk in chunks:
        chunk["dependencies"] = []

    for dependency in dependencies:

        dependency_line = dependency["line"]

        for chunk in chunks:

            if (
                chunk["start_line"]
                <= dependency_line
                <= chunk["end_line"]
            ):

                chunk["dependencies"].append(
                    dependency["target"]
                )

                break

    return chunks