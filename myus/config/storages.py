from django.conf import settings
from django.core import signing
from django.core.files.storage import FileSystemStorage


PRIVATE_URL_SALT = "private"


class SignedFileSystemStorage(FileSystemStorage):
    def url(self, name: str | None) -> str:
        token = signing.dumps(name, salt=PRIVATE_URL_SALT)
        return f"{settings.DOMAIN_URL}/private/{token}"
