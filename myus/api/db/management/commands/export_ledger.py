import csv
from datetime import date, datetime, time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.modules.logger import log
from api.src.usecase.payment import export_ledger


LEDGER_CSV_HEADER = ["日時", "決済会社", "種類", "金額", "消費税額", "通貨", "取引ID", "請求書番号", "入金ID", "入金日"]


class Command(BaseCommand):
    help = "期間を指定して、帳簿の明細を CSV で出す（日付は日本時間。--to の日も含む）"

    def add_arguments(self, parser):
        parser.add_argument("--from", dest="date_from", type=date.fromisoformat, required=True, help="開始日（例: 2026-01-01）")
        parser.add_argument("--to", dest="date_to", type=date.fromisoformat, required=True, help="終了日（例: 2026-12-31）")

    def handle(self, *args, **options):
        start = timezone.make_aware(datetime.combine(options["date_from"], time.min))
        end = timezone.make_aware(datetime.combine(options["date_to"] + timedelta(days=1), time.min))

        ret = export_ledger(start, end)
        if ret.is_err:
            log.error("Ledger export command failed", error=ret.err_value.message)
            self.stderr.write(self.style.ERROR("帳簿の出力に失敗しました"))
            return

        rows = ret.ok_value
        writer = csv.writer(self.stdout)
        writer.writerow(LEDGER_CSV_HEADER)
        for row in rows:
            writer.writerow([
                timezone.localtime(row.occurred_at).strftime("%Y-%m-%d %H:%M:%S"),
                row.provider.value,
                row.entry_type.value,
                row.amount,
                row.tax_amount,
                row.currency.value.upper(),
                row.transaction_external_id,
                row.receipt_number,
                row.payout_external_id,
                timezone.localtime(row.payout_arrival_at).strftime("%Y-%m-%d") if row.payout_arrival_at is not None else "",
            ])
