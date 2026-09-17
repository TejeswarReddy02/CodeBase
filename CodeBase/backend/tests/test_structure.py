from app.repository.reader import read_repository
from app.chunking.structure import (
    extract_structure,
    extract_project_dependencies
)


repository_path = (
    r"C:\FinalYearProject\CodeBase\data\repositories\laptop-price-predictor"
)


files = read_repository(repository_path)


for file_data in files:

    print("\n" + "=" * 60)

    print(
        f"FILE: {file_data['file_path']}"
    )

    if file_data["language"] != "python":
        continue

    structure = extract_structure(
        file_data["content"]
    )

    print("\nIMPORTS:")

    for item in structure["imports"]:
        print(" ", item)

    print("\nFUNCTIONS:")

    for item in structure["functions"]:
        print(
            f"  {item['name']} "
            f"({item['start_line']}-{item['end_line']})"
        )

    print("\nCLASSES:")

    for item in structure["classes"]:
        print(
            f"  {item['name']} "
            f"({item['start_line']}-{item['end_line']})"
        )

    print("\nMETHODS:")

    for item in structure["methods"]:
        print(
            f"  {item['class_name']}.{item['name']} "
            f"({item['start_line']}-{item['end_line']})"
        )

    print("\nPROJECT DEPENDENCIES:")

    dependencies = extract_project_dependencies(
        file_data["content"],
        structure
    )

    for dependency in dependencies:

        source = dependency["source"]

        source_name = (
            source["name"]
            if source["name"]
            else "module"
        )

        print(
            f"  {source['type']} "
            f"{source_name} "
            f"-> {dependency['target']} "
            f"(line {dependency['line']})"
        )