import json
from pathlib import Path
from typing import Any, get_args
from pydantic import TypeAdapter
from config.env import BASE_DIR
from api.src.domain.interface.payment.event.data import PaymentEventContent


PAYMENT_EVENT_SCHEMA_DIR = Path(BASE_DIR) / "api" / "tests" / "payment_event_schema"


def payment_event_schemas() -> dict[str, dict[str, Any]]:
    return {content.__name__: TypeAdapter(content).json_schema() for content in get_args(PaymentEventContent.__value__)}


def payment_event_schema_path(name: str) -> Path:
    return PAYMENT_EVENT_SCHEMA_DIR / f"{name}.json"


def read_payment_event_schema(name: str) -> dict[str, Any]:
    path = payment_event_schema_path(name)
    if not path.exists():
        return {}

    schema: dict[str, Any] = json.loads(path.read_text())
    return schema


def write_payment_event_schema(name: str, schema: dict[str, Any]) -> None:
    payment_event_schema_path(name).write_text(json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def schema_breaking_changes(saved: dict[str, Any], current: dict[str, Any]) -> list[str]:
    return compare_schema(saved, current, saved.get("$defs", {}), current.get("$defs", {}), "")


def compare_schema(saved: dict[str, Any], current: dict[str, Any], saved_defs: dict[str, Any], current_defs: dict[str, Any], path: str) -> list[str]:
    saved = resolve_schema(saved, saved_defs)
    current = resolve_schema(current, current_defs)
    if saved.get("type") != current.get("type") or saved.get("format") != current.get("format"):
        return [f"{path}: 型が {saved.get('type')}（{saved.get('format')}）から {current.get('type')}（{current.get('format')}）に変わった"]

    changes = [f"{path}: 値 {value} が消えた" for value in saved.get("enum", []) if value not in current.get("enum", [])]
    current_properties = current.get("properties", {})
    for name, saved_property in saved.get("properties", {}).items():
        if name not in current_properties:
            changes.append(f"{path}.{name}: 項目が消えた")
            continue
        changes.extend(compare_schema(saved_property, current_properties[name], saved_defs, current_defs, f"{path}.{name}"))

    changes.extend(f"{path}.{name}: 必須の項目が増えた" for name in current.get("required", []) if name not in saved.get("required", []))
    if "items" in saved:
        changes.extend(compare_schema(saved["items"], current.get("items", {}), saved_defs, current_defs, f"{path}[]"))
    return changes


def resolve_schema(schema: dict[str, Any], defs: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref", "")
    if len(ref) == 0:
        return schema

    definition: dict[str, Any] = defs[ref.removeprefix("#/$defs/")]
    return definition
