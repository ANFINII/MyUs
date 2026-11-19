import sys
from django.core.management.base import BaseCommand
from django.db import connection
from myus.utils.common.logger import log


class Command(BaseCommand):
    help = "標準入力の SQL を1文ずつ流す。PR に書いたスキーマの変更を本番の DB に当てるときに使う"

    def handle(self, *args, **options):
        statements = connection.ops.prepare_sql_script(sys.stdin.read())
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
                log.info("executed", statement=statement)
