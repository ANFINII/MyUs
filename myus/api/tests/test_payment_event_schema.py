import pytest
from api.utils.functions.schema import payment_event_schema_path, payment_event_schemas, read_payment_event_schema, schema_breaking_changes


@pytest.mark.parametrize("name", payment_event_schemas().keys())
def test_payment_event_schema_is_compatible(name: str) -> None:
    assert payment_event_schema_path(name).exists(), f"{name} のスキーマがありません。manage.py export_payment_event_schema を実行してください"
    assert schema_breaking_changes(read_payment_event_schema(name), payment_event_schemas()[name]) == []


def test_removed_property_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string"}}, "required": ["amount", "memo"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}

    assert schema_breaking_changes(saved, current) == [".memo: 項目が消えた"]


def test_changed_type_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "string"}}, "required": ["amount"]}

    assert schema_breaking_changes(saved, current) == [".amount: 型が integer（None）から string（None）に変わった"]


def test_new_required_property_is_breaking() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string"}}, "required": ["amount", "memo"]}

    assert schema_breaking_changes(saved, current) == [".memo: 必須の項目が増えた"]


def test_removed_enum_value_is_breaking() -> None:
    saved = {"type": "object", "properties": {"status": {"$ref": "#/$defs/Status"}}, "required": ["status"], "$defs": {"Status": {"type": "string", "enum": ["Paid", "Failed"]}}}
    current = {"type": "object", "properties": {"status": {"$ref": "#/$defs/Status"}}, "required": ["status"], "$defs": {"Status": {"type": "string", "enum": ["Paid"]}}}

    assert schema_breaking_changes(saved, current) == [".status: 値 Failed が消えた"]


def test_new_optional_property_is_compatible() -> None:
    saved = {"type": "object", "properties": {"amount": {"type": "integer"}}, "required": ["amount"]}
    current = {"type": "object", "properties": {"amount": {"type": "integer"}, "memo": {"type": "string", "default": ""}}, "required": ["amount"]}

    assert schema_breaking_changes(saved, current) == []
