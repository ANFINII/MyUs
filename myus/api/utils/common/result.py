from __future__ import annotations

from collections.abc import Callable
from typing import final


class _Nil:
    """
    Resultのnil状態を表すクラス
    Noneと混同しないこと：TがNoneの場合、ok_valueはNoneでerr_valueはNil
    """

    pass


@final
class Result[T, E]:
    """成功(Ok)または失敗(Err)を表すResult型"""

    __dummy = object()

    def __init__(
        self,
        dummy: object,
        *,
        is_ok: bool,
        ok_value: T | _Nil,
        err_value: E | _Nil,
    ) -> None:
        if dummy is not Result.__dummy:
            raise RuntimeError(
                "Resultインスタンスを直接作成しないでください。"
                "代わりにResult.ok()またはResult.err()を使用してください"
            )

        self._is_ok = is_ok
        self._ok_value = ok_value
        self._err_value = err_value

        if is_ok:
            assert isinstance(err_value, _Nil)
        else:
            assert isinstance(ok_value, _Nil)

    def __str__(self) -> str:
        if self._is_ok:
            return f"Result[ok={self.ok_value!s}]"
        return f"Result[err={self.err_value!s}]"

    def __repr__(self) -> str:
        if self._is_ok:
            return f"Result[ok={self.ok_value!r}]"
        return f"Result[err={self.err_value!r}]"

    # ファクトリメソッド
    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        """成功値を持つResultを作成"""
        return Result[T, E](Result.__dummy, is_ok=True, ok_value=value, err_value=_Nil())

    @classmethod
    def err(cls, value: E) -> Result[T, E]:
        """エラー値を持つResultを作成"""
        return Result[T, E](Result.__dummy, is_ok=False, ok_value=_Nil(), err_value=value)

    # 状態確認
    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_err(self) -> bool:
        return not self._is_ok

    # 値の取得
    @property
    def ok_value(self) -> T:
        """成功値を取得（Errの場合はRuntimeError）"""
        if not self._is_ok:
            raise RuntimeError("結果がerrの場合はok_valueにアクセスしないでください")
        assert not isinstance(self._ok_value, _Nil)
        return self._ok_value

    @property
    def err_value(self) -> E:
        """エラー値を取得（Okの場合はRuntimeError）"""
        if self._is_ok:
            raise RuntimeError("結果がokの場合はerr_valueにアクセスしないでください")
        assert not isinstance(self._err_value, _Nil)
        return self._err_value

    def maybe_ok(self) -> T | None:
        """OkならばTを返し、ErrならばNoneを返す"""
        if self._is_ok:
            return self.ok_value
        return None

    def maybe_err(self) -> E | None:
        """Errならばerr_valueを返し、OkならばNoneを返す"""
        if not self._is_ok:
            return self.err_value
        return None

    # 変換メソッド
    def map[U](self, fn: Callable[[T], U]) -> Result[U, E]:
        """Okならば値を関数fnで変換し、Errならばそのまま返す"""
        if self._is_ok:
            return Result.ok(fn(self.ok_value))
        return Result.err(self.err_value)

    def map_err[F](self, fn: Callable[[E], F]) -> Result[T, F]:
        """Errならばエラーを関数fnで変換し、Okならばそのまま返す"""
        if self._is_ok:
            return Result.ok(self.ok_value)
        return Result.err(fn(self.err_value))

    def and_then[U](self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Okならば値を渡してResultを返す関数fnを呼び出し、Errならばそのまま返す"""
        if self._is_ok:
            return fn(self.ok_value)
        return Result.err(self.err_value)

    # アンラップ
    def ok_or(self, default: T) -> T:
        """Okならばその値を返し、Errならばdefaultを返す"""
        if self._is_ok:
            return self.ok_value
        return default

    def ok_or_else(self, fn: Callable[[E], T]) -> T:
        """Okならばその値を返し、Errならば関数fnにerr_valueを渡してその結果を返す"""
        if self._is_ok:
            return self.ok_value
        return fn(self.err_value)

    def expect(self, msg: str) -> T:
        """Okならばok_valueを返し、ErrならばAssertionErrorを発生

        絶対にOkでなければおかしいロジックの場合のみ使用
        """
        assert self._is_ok, msg
        return self.ok_value

    # テスト用ヘルパー
    def assert_ok(self) -> T:
        """テスト用: Okであることを確認し、値を返す"""
        assert self._is_ok, f"Expected Ok, but got Err: {self._err_value}"
        return self.ok_value

    def assert_err(self) -> E:
        """テスト用: Errであることを確認し、エラーを返す"""
        assert not self._is_ok, f"Expected Err, but got Ok: {self._ok_value}"
        return self.err_value

    def assert_ok_value(self, expected: T) -> None:
        """テスト用: Okかつ値が一致するかを確認"""
        assert self._is_ok, f"Expected Ok, but got Err: {self._err_value}"
        assert self.ok_value == expected, f"Expected {expected}, but got {self.ok_value}"

    def assert_err_value(self, expected: E) -> None:
        """テスト用: Errかつ値が一致するかを確認"""
        assert not self._is_ok, f"Expected Err, but got Ok: {self._ok_value}"
        assert self.err_value == expected, f"Expected {expected}, but got {self.err_value}"

    def assert_err_type(self, expected_type: type[E]) -> None:
        """テスト用: Errかつ型が一致するかを確認"""
        assert not self._is_ok, f"Expected Err, but got Ok: {self._ok_value}"
        assert type(self.err_value) is expected_type, f"Expected {expected_type}, but got {type(self.err_value)}"
