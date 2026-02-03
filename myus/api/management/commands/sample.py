from django.core.management.base import BaseCommand
from api.utils.enum.index import CommentType, CommentTypeNo
from api.utils.functions.map import comment_type_map, comment_type_no_map


class Command(BaseCommand):
    help = 'コマンドの説明（manage.py help に表示されます）'

    def add_arguments(self, parser):
        # 引数の追加（必要な場合）
        parser.add_argument('--name', type=str, help='名前を指定します')

    def handle(self, *args, **options):
        name = options.get('name', 'World')

        video_no = CommentTypeNo.VIDEO
        video_name = comment_type_map(video_no)

        music_name = CommentType.MUSIC
        music_no = comment_type_no_map(music_name)

        print(video_name)
        print(music_no)
        self.stdout.write(self.style.SUCCESS(f'Hello, {name}!'))
