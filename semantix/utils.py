import re
from enum import Enum
from typing import Any
import sys
import inspect
import ast


def get_type(_type: Any) -> str:  # noqa: ANN401
    if hasattr(_type, "__origin__") and _type.__origin__ is not None:
        if _type.__origin__ == list:
            return f"list[{get_type(_type.__args__[0])}]"
        if _type.__origin__ == dict:
            return f"dict[{get_type(_type.__args__[0])}, {get_type(_type.__args__[1])}]"
        if _type.__origin__ == tuple:
            return f"tuple[{', '.join([get_type(x) for x in _type.__args__])}]"
        if _type.__origin__ == set:
            return f"set[{get_type(_type.__args[0])}]"
    return str(_type.__name__) if isinstance(_type, type) else str(_type)


def get_object_string(obj: Any) -> str:  # noqa: ANN401
    """Get the string representation of the input object."""
    if isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float, bool)):
        return str(obj)
    elif isinstance(obj, list):
        return "[" + ", ".join(get_object_string(item) for item in obj) + "]"
    elif isinstance(obj, tuple):
        return "(" + ", ".join(get_object_string(item) for item in obj) + ")"
    elif isinstance(obj, dict):
        return (
            "{"
            + ", ".join(
                f"{get_object_string(key)}: {get_object_string(value)}"
                for key, value in obj.items()
            )
            + "}"
        )
    elif isinstance(obj, Enum):
        return f"{obj.__class__.__name__}.{obj.name}"
    elif hasattr(obj, "__dict__"):
        args = ", ".join(
            f"{key}={get_object_string(value)}" for key, value in vars(obj).items()
        )
        return f"{obj.__class__.__name__}({args})"
    else:
        return str(obj)


def extract_non_primary_type(type_str: str) -> list:
    """Extract non-primary types from the type string."""
    if not type_str:
        return []
    pattern = r"(?:\[|,\s*|\|)([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)"
    matches = re.findall(pattern, type_str)
    primary_types = [
        "str",
        "int",
        "float",
        "bool",
        "list",
        "dict",
        "tuple",
        "set",
        "Any",
        "None",
    ]
    non_primary_types = [m for t in matches for m in t if m and m not in primary_types]
    return non_primary_types


def get_type_from_value(data: Any) -> str:  # noqa: ANN401
    """Get the type annotation of the input data."""
    if isinstance(data, dict):
        class_name = next(
            (value.__class__.__name__ for value in data.values() if value is not None),
            None,
        )
        if class_name:
            return f"dict[str, {class_name}]"
        else:
            return "dict[str, Any]"
    elif isinstance(data, list):
        if data:
            class_name = data[0].__class__.__name__
            return f"list[{class_name}]"
        else:
            return "list"
    else:
        return str(type(data).__name__)


def get_meaning(obj, var_name="", module=""):
    frame = inspect.currentframe().f_back
    var_name = (
        next((var for var, val in frame.f_locals.items() if val is obj), None)
        if not var_name
        else var_name
    )
    _module = sys.modules[frame.f_globals["__name__"]] if not module else module

    if var_name:
        meaning = getattr(_module, f"{var_name}_meaning", None)
    if not meaning and var_name:
        with open(frame.f_code.co_filename, "r") as file:
            tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == var_name:
                        module = importlib.import_module(node.module)
                        meaning = get_meaning(obj, var_name, module)
                        break
    return meaning
