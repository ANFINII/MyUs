from django.core.management.base import BaseCommand
from api.utils.functions.schema import event_schemas, read_schema, schema_breaking_changes, write_schema


class Command(BaseCommand):
    help = "PaymentEvent の content と集約のイベントの JSON スキーマを api/tests/payment_event_schema・es_event_schema に出す。過去のイベントを読めなくなる変更は書き出さない"

    def handle(self, *args, **options):
        for path, schema in event_schemas().items():
            saved = read_schema(path)
            changes = schema_breaking_changes(saved, schema) if len(saved) > 0 else []
            if len(changes) > 0:
                self.stderr.write(self.style.ERROR(f"{path.stem} は過去のイベントを読めなくなる変更のため書き出しません: {', '.join(changes)}"))
                continue

            write_schema(path, schema)
            self.stdout.write(self.style.SUCCESS(f"Exported {path.stem}"))
