from app.repository.reader import read_repository
from app.chunking.structure import (
    extract_structure,
    extract_project_dependencies
)
from app.chunking.chunker import (
    create_chunks,
    attach_dependencies
)

repository_path = (
    r"C:\FinalYearProject\CodeBase\data\repositories\laptop-price-predictor"
)


files = read_repository(repository_path)


for file_data in files:

    if file_data["language"] != "python":
        continue

    structure = extract_structure(
        file_data["content"]
    )

    chunks = create_chunks(
        source_code=file_data["content"],
        file_path=file_data["file_path"],
        language=file_data["language"],
        structure=structure
    )
    dependencies = extract_project_dependencies(
    file_data["content"],
    structure
    )

    chunks = attach_dependencies(
        chunks,
        dependencies
    )

    print("\n" + "=" * 60)

    print(
        f"FILE: {file_data['file_path']}"
    )

    print(
        f"TOTAL CHUNKS: {len(chunks)}"
    )

    for chunk in chunks:

            print("\n" + "=" * 60)

    print(
        f"FILE: {file_data['file_path']}"
    )

    print(
        f"TOTAL CHUNKS: {len(chunks)}"
    )

    for chunk in chunks:

        print("\n" + "-" * 60)

        print(
            f"ID: {chunk['chunk_id']}"
        )

        print(
            f"TYPE: {chunk['chunk_type']}"
        )

        print(
            f"NAME: {chunk['name']}"
        )

        print(
            f"LINES: "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )

        print("\nEMBEDDING TEXT:")

        print(chunk["embedding_text"])
        
    for chunk in chunks:

        print(
            chunk["chunk_type"],
            chunk["name"],
            f"({chunk['start_line']}-{chunk['end_line']})"
        )

        print(
            "Dependencies:",
            chunk["dependencies"]
        )

        print()