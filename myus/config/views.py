import mimetypes
import re
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseBase


def serve_media(request: HttpRequest, path: str) -> HttpResponseBase:
    """Range対応のメディアファイル配信"""

    file_path = Path(settings.MEDIA_ROOT) / path
    if not file_path.resolve().is_relative_to(Path(settings.MEDIA_ROOT).resolve()):
        return HttpResponse(status=403)

    if not file_path.exists():
        return HttpResponse(status=404)

    file_size = file_path.stat().st_size
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

    range_header = request.META.get("HTTP_RANGE")
    if range_header is not None:
        parsed = _parse_range(range_header, file_size)
        if parsed is not None:
            start, end = parsed
            length = end - start + 1

            with open(file_path, "rb") as f:
                f.seek(start)
                data = f.read(length)

            response = HttpResponse(data, status=206, content_type=content_type)
            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            response["Content-Length"] = length
            response["Accept-Ranges"] = "bytes"
            return response

    file_response = FileResponse(open(file_path, "rb"), content_type=content_type)
    file_response["Accept-Ranges"] = "bytes"
    file_response["Content-Length"] = file_size
    return file_response


def _parse_range(header: str, file_size: int) -> tuple[int, int] | None:
    """Range headerをパースして(start, end)を返す"""

    match = re.match(r"bytes=(\d+)-(\d*)", header)
    if match is None:
        return None

    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else file_size - 1
    return start, min(end, file_size - 1)
