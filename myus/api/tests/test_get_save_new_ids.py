from typing import Any
import pytest
from django.db import transaction
from django.db.models.query import QuerySet
from api.db.models.master import NgWord
from api.src.domain.entity.index import get_save_new_ids


def words() -> list[str]:
    return list(NgWord.objects.order_by("id").values_list("word", flat=True))


@pytest.mark.django_db
def test_new_rows_are_inserted_and_ids_returned() -> None:
    new_ids = get_save_new_ids([NgWord(word="a"), NgWord(word="b")], ["word"])

    assert new_ids == list(NgWord.objects.order_by("id").values_list("id", flat=True))
    assert words() == ["a", "b"]


@pytest.mark.django_db
def test_existing_rows_are_updated_and_only_new_ids_returned() -> None:
    existing = NgWord.objects.create(word="a")
    existing.word = "a-updated"

    new_ids = get_save_new_ids([existing, NgWord(word="b")], ["word"])

    assert len(new_ids) == 1
    assert NgWord.objects.get(id=new_ids[0]).word == "b"
    assert words() == ["a-updated", "b"]


@pytest.mark.django_db
def test_rollback_removes_inserted_rows() -> None:
    with transaction.atomic():
        get_save_new_ids([NgWord(word="a")], ["word"])
        transaction.set_rollback(True)

    assert words() == []


@pytest.mark.django_db
def test_upsert_failure_rolls_back_inserted_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    existing = NgWord.objects.create(word="a")
    existing.word = "a-updated"

    def failing_bulk_create(self: QuerySet[Any], *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("upsert failed")

    monkeypatch.setattr(QuerySet, "bulk_create", failing_bulk_create)

    with pytest.raises(RuntimeError):
        get_save_new_ids([existing, NgWord(word="b")], ["word"])

    assert words() == ["a"]
