from django.core.management.base import BaseCommand
from api.utils.functions.schema import payment_event_schemas, read_payment_event_schema, schema_breaking_changes, write_payment_event_schema


class Command(BaseCommand):
    help = "PaymentEvent の content の JSON スキーマを api/tests/payment_event_schema に出す。過去のイベントを読めなくなる変更は書き出さない"

    def handle(self, *args, **options):
        for name, schema in payment_event_schemas().items():
            saved = read_payment_event_schema(name)
            changes = schema_breaking_changes(saved, schema) if len(saved) > 0 else []
            if len(changes) > 0:
                self.stderr.write(self.style.ERROR(f"{name} は過去のイベントを読めなくなる変更のため書き出しません: {', '.join(changes)}"))
                continue

            write_payment_event_schema(name, schema)
            self.stdout.write(self.style.SUCCESS(f"Exported {name}"))
