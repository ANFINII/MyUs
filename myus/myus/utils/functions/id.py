from django_ulid.models import ulid


def new_ulid() -> str:
    return str(ulid.new())
