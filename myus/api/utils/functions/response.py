from dataclasses import asdict, is_dataclass
from typing import Any, Optional
from rest_framework.response import Response


def dataclass_dict(instance: Any) -> Any:
    """
    任意のdataclassインスタンスを再帰的に辞書に変換します。
    辞書やリストもサポートし、ネストされた構造を保持します。

    Parameters: instance (Any): dataclassインスタンスまたは通常のリストや辞書
    Returns: Any: 辞書形式に変換されたデータ
    """

    if is_dataclass(instance):
        return {k: dataclass_dict(v) for k, v in asdict(instance).items()}
    elif isinstance(instance, dict):
        return {k: dataclass_dict(v) for k, v in instance.items()}
    elif isinstance(instance, list):
        return [dataclass_dict(item) for item in instance]
    else:
        return instance


class DataResponse(Response):
    def __init__(self, data: Any, status: Optional[int], **kwargs):
        super().__init__(dataclass_dict(data), status=status, **kwargs)
