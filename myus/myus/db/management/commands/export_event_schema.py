from pathlib import Path
from typing import Any, get_args
from pydantic import TypeAdapter
from django.core.management.base import BaseCommand
from config.env import BASE_DIR
from myus.domain.aggregate.subscription.event import SUBSCRIPTION_EVENT_CLASSES
from myus.domain.interface.payment.event.data import PaymentEventContent
from myus.utils.functions.schema_compatibility import breaking_changes, read_schema, write_schema


SCHEMA_COMPATIBILITY_DIR = Path(BASE_DIR) / "myus" / "tests" / "schema_compatibility"


def event_schemas() -> dict[Path, dict[str, Any]]:
    payment_schemas = {SCHEMA_COMPATIBILITY_DIR / "payment_event" / f"{content.__name__}.json": TypeAdapter(content).json_schema() for content in get_args(PaymentEventContent.__value__)}
    es_schemas = {SCHEMA_COMPATIBILITY_DIR / "es_event" / f"{event_type}.json": TypeAdapter(event_class).json_schema() for event_type, event_class in SUBSCRIPTION_EVENT_CLASSES.items()}
    return payment_schemas | es_schemas


class Command(BaseCommand):
    help = "PaymentEvent の content と集約のイベントの JSON スキーマを myus/tests/schema_compatibility に出す。過去のイベントを読めなくなる変更は書き出さない"

    def handle(self, *args, **options):
        for path, schema in event_schemas().items():
            saved = read_schema(path)
            changes = breaking_changes(saved, schema) if len(saved) > 0 else []
            if len(changes) > 0:
                self.stderr.write(self.style.ERROR(f"{path.stem} は過去のイベントを読めなくなる変更のため書き出しません: {', '.join(changes)}"))
                continue

            write_schema(path, schema)
            self.stdout.write(self.style.SUCCESS(f"Exported {path.stem}"))
