import os
from dataclasses import fields, is_dataclass
from dacite import Config, from_dict
from enum import Enum
from pathlib import Path
from typing import Any, TypeVar, cast, get_args, get_origin

T = TypeVar("T")


def new(dataclass_type: type[T], src: dict[str, Any] | None = None, enums: list[type[Enum]] | None = None) -> T:
    """環境変数からdataclassのインスタンスを生成する"""

    if src is None:
        src = {key.lower(): value for key, value in os.environ.items()}
    if enums is None:
        enums = []

    if not is_dataclass(dataclass_type):
        raise TypeError(f"{dataclass_type} is not a dataclass")

    class_attrs = vars(dataclass_type)
    class_attrs_set = {k for k, v in class_attrs.items() if not callable(v)}
    instance_fields = {field.name for field in fields(dataclass_type)}
    class_vars = {key for key in class_attrs_set if key not in instance_fields and not key.startswith("__")}
    assert not class_vars, f"dataclassに何故かクラス変数が混ざっています!! {class_vars}"

    result = from_dict(
        data_class=dataclass_type,
        data=src,
        config=Config(
            cast=enums,
            type_hooks={
                list[int]: lambda v: _type_converter(v, list[int]),
                list[str]: lambda v: _type_converter(v, list[str]),
                list[float]: lambda v: _type_converter(v, list[float]),
                list[bool]: lambda v: _type_converter(v, list[bool]),
                int: lambda v: _type_converter(v, int),
                bool: lambda v: _type_converter(v, bool),
                float: lambda v: _type_converter(v, float),
                Path: lambda v: _type_converter(v, Path),
            },
        ),
    )

    return cast(T, result)


def _type_converter(value: Any, target_type: type[Any]) -> Any:
    origin = get_origin(target_type)
    args = get_args(target_type)

    if origin is not None:
        if origin is list:
            if isinstance(value, str):
                if len(value.strip()) == 0:
                    return []
                parsed_value = [v.strip() for v in value.split(",")]
                if isinstance(parsed_value, list):
                    inner_type = args[0]
                    return [_type_converter(v, inner_type) for v in parsed_value]
                raise ValueError(f"Cannot convert {value} to list")
            if isinstance(value, list):
                inner_type = args[0]
                return [_type_converter(v, inner_type) for v in value]
        raise AssertionError("非サポートの変換です！")

    if isinstance(value, target_type):
        return value

    if isinstance(value, str):
        if target_type is int:
            return int(value)
        if target_type is bool:
            v = value.lower().strip()
            if v in {"true", "1", "yes"}:
                return True
            if v in {"false", "0", "no"}:
                return False
            raise AssertionError(f"boolに変換できない値が入っています: {value}")
        if target_type is float:
            return float(value)
        if target_type == Path:
            return Path(value)

    raise AssertionError(f"Unknown type for conversion: {target_type}")
