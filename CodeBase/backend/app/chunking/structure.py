from tree_sitter import Language, Parser
import tree_sitter_python as tspython


PYTHON_LANGUAGE = Language(tspython.language())


def create_parser() -> Parser:
    return Parser(PYTHON_LANGUAGE)


def parse_code(source_code: str):
    parser = create_parser()

    source_bytes = source_code.encode("utf-8")

    return parser.parse(source_bytes)


def extract_structure(source_code: str) -> dict:
    tree = parse_code(source_code)

    root = tree.root_node

    structure = {
        "imports": [],
        "functions": [],
        "classes": [],
        "methods": []
    }

    def walk(node, current_class=None):

        if node.type == "import_statement":
            structure["imports"].append(
                source_code[
                    node.start_byte:node.end_byte
                ]
            )

        elif node.type == "import_from_statement":
            structure["imports"].append(
                source_code[
                    node.start_byte:node.end_byte
                ]
            )

        elif node.type == "function_definition":

            name_node = node.child_by_field_name("name")

            if name_node is not None:
                name = source_code[
                    name_node.start_byte:name_node.end_byte
                ]

                item = {
                    "name": name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1
                }

                if current_class:
                    item["class_name"] = current_class
                    structure["methods"].append(item)
                else:
                    structure["functions"].append(item)

        elif node.type == "class_definition":

            name_node = node.child_by_field_name("name")

            if name_node is not None:
                name = source_code[
                    name_node.start_byte:name_node.end_byte
                ]

                structure["classes"].append(
                    {
                        "name": name,
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1
                    }
                )

                current_class = name

        for child in node.children:
            walk(child, current_class)

    walk(root)

    return structure


def extract_function_calls(source_code: str) -> list[str]:
    tree = parse_code(source_code)

    calls = []

    def walk(node):

        if node.type == "call":

            function_node = node.child_by_field_name("function")

            if function_node is not None:

                function_name = source_code[
                    function_node.start_byte:
                    function_node.end_byte
                ]

                calls.append(function_name)

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return calls


def extract_project_dependencies(
    source_code: str,
    structure: dict
) -> list[dict]:

    defined_functions = {
        function["name"]
        for function in structure["functions"]
    }

    defined_functions.update(
        method["name"]
        for method in structure["methods"]
    )

    dependencies = []

    tree = parse_code(source_code)

    def get_code_region(node):
        """
        Determine the nearest meaningful code region
        containing this reference.
        """

        current = node.parent

        while current is not None:

            if current.type == "function_definition":
                name_node = current.child_by_field_name("name")

                if name_node is not None:
                    name = source_code[
                        name_node.start_byte:
                        name_node.end_byte
                    ]

                    return {
                        "type": "function",
                        "name": name,
                        "start_line": current.start_point[0] + 1,
                        "end_line": current.end_point[0] + 1
                    }

            if current.type == "class_definition":
                name_node = current.child_by_field_name("name")

                if name_node is not None:
                    name = source_code[
                        name_node.start_byte:
                        name_node.end_byte
                    ]

                    return {
                        "type": "class",
                        "name": name,
                        "start_line": current.start_point[0] + 1,
                        "end_line": current.end_point[0] + 1
                    }

            current = current.parent

        return {
            "type": "module",
            "name": None,
            "start_line": 1,
            "end_line": len(source_code.splitlines())
        }

    def walk(node):

        if node.type == "identifier":

            name = source_code[
                node.start_byte:
                node.end_byte
            ]

            if name in defined_functions:

                parent = node.parent

                # Ignore the function definition itself.
                if (
                    parent is not None
                    and parent.type == "function_definition"
                    and parent.child_by_field_name("name") == node
                ):
                    pass

                else:

                    region = get_code_region(node)

                    dependencies.append(
                        {
                            "source": region,
                            "target": name,
                            "line": node.start_point[0] + 1
                        }
                    )

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return dependencies