from django.core.management.base import BaseCommand, CommandError
from api.src.routers import api


ALLOWED_STATUS = {200, 400, 500}


class Command(BaseCommand):
    help = "API のレスポンスのステータスが 200 / 400 / 500 だけであることを確かめる"

    def handle(self, *args, **options):
        schema = api.get_openapi_schema()

        violations = []
        for path, operations in schema["paths"].items():
            for method, operation in operations.items():
                for status in operation["responses"]:
                    if int(status) not in ALLOWED_STATUS:
                        violations.append(f"{method.upper()} {path}: {status}")

        if len(violations) > 0:
            raise CommandError("Disallowed response status found\n" + "\n".join(violations))

        self.stdout.write("OK")
