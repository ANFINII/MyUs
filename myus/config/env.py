import os
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar
from config.dataclass_env import new

T = TypeVar("T")

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = Path("envs/django.env")


@dataclass(frozen=True)
class Environment:
    # Django
    secret_key: str
    debug: bool
    allowed_hosts: list[str]
    cors_allowed_origins: list[str]
    csrf_trusted_origins: list[str]
    domain_url: str
    encrypt_key: str
    encrypt_iv: str

    # MySQL
    mysql_engine: str
    mysql_database: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_root_password: str
    mysql_conn_max_age: int
    database_url: str

    # Redis
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str
    redis_url: str

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_storage_bucket_name: str
    aws_s3_custom_domain: str
    aws_s3_region_name: str
    aws_region_log: str
    aws_ses_access_key_id: str
    aws_ses_secret_access_key: str

    # Email
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str

    # Stripe
    stripe_secret_key: str
    stripe_public_key: str
    stripe_webhook_secret: str
    stripe_cli: str
    stripe_live_mode: bool


def load_env(env_path: Path) -> None:
    """envファイルから環境変数を読み込む"""
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


load_env(BASE_DIR / ENV_PATH)
env = new(Environment)
