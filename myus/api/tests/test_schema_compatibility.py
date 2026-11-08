from pathlib import Path
import pytest
from api.db.management.commands.export_event_schema import event_schemas
from api.utils.functions.schema_compatibility import breaking_changes, read_schema


@pytest.mark.parametrize("path", event_schemas().keys(), ids=lambda path: path.stem)
def test_event_schema_is_compatible(path: Path) -> None:
    assert path.exists(), f"{path.stem} のスキーマがありません。manage.py export_event_schema を実行してください"
    assert breaking_changes(read_schema(path), event_schemas()[path]) == []


def test_removed_property_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string"}}, "required": ["amount", "memo"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}

    assert breaking_changes(saved, current) == [".memo: 項目が消えた"]


def test_changed_type_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "string"}}, "required": ["amount"]}

    assert breaking_changes(saved, current) == [".amount: 型が integer（None）から string（None）に変わった"]


def test_new_required_property_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string"}}, "required": ["amount", "memo"]}

    assert breaking_changes(saved, current) == [".memo: 必須の項目が増えた"]


def test_removed_enum_value_is_breaking() -> None:
    saved = {"type": "object", "properties": {"status": {"$ref": "#/$defs/Status"}}, "required": ["status"], "$defs": {"Status": {"type": "string", "enum": ["Paid", "Failed"]}}}
    current = {"type": "object", "properties": {"status": {"$ref": "#/$defs/Status"}}, "required": ["status"], "$defs": {"Status": {"type": "string", "enum": ["Paid"]}}}

    assert breaking_changes(saved, current) == [".status: 値 Failed が消えた"]


def test_new_optional_property_is_compatible() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string", "default": ""}}, "required": ["amount"]}

    assert breaking_changes(saved, current) == []
