from __future__ import annotations

from collections.abc import Callable


class _Nil:
    """_Resultのnil状態を表す内部クラス。
    is_okの場合はerr_valueが_Nil、is_errの場合はok_valueが_Nil。
    Noneと区別するために専用クラスを用意している。
    """


class _Result[T, E]:
    """Rust の Result<T, E> に相当する内部実装。

    直接インスタンス化せず、ok / err クラスメソッドを使う。
    """

    __dummy = object()

    def __init__(
        self,
        dummy: object,
        *,
        is_ok: bool,
        ok_value: T | _Nil,
        err_value: E | _Nil,
    ) -> None:
        if dummy is not _Result.__dummy:
            raise RuntimeError(
                "_Resultインスタンスを直接作成しないでください。_Result.okまたは_Result.errを使用してください"
            )

        self._is_ok = is_ok
        self._ok_value = ok_value
        self._err_value = err_value

        if is_ok:
            assert isinstance(err_value, _Nil)
        else:
            assert isinstance(ok_value, _Nil)

    def __str__(self) -> str:
        if self.is_ok:
            return f"_Result[ok={self.ok_value!s}]"
        return f"_Result[err={self.err_value!s}]"

    def __repr__(self) -> str:
        if self.is_ok:
            return f"_Result[ok={self.ok_value!r}]"
        return f"_Result[err={self.err_value!r}]"

    @classmethod
    def ok(cls, value: T) -> _Result[T, E]:
        return _Result[T, E](_Result.__dummy, is_ok=True, ok_value=value, err_value=_Nil())

    @classmethod
    def err(cls, value: E) -> _Result[T, E]:
        return _Result[T, E](_Result.__dummy, is_ok=False, ok_value=_Nil(), err_value=value)

    def maybe_ok(self) -> T | None:
        if self.is_ok:
            return self.ok_value
        return None

    def maybe_err(self) -> E | None:
        if self.is_err:
            return self.err_value
        return None

    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_err(self) -> bool:
        return not self._is_ok

    @property
    def ok_value(self) -> T:
        if not self._is_ok:
            raise RuntimeError("結果がerrの場合はok_valueにアクセスしないでください")
        assert not isinstance(self._ok_value, _Nil)
        return self._ok_value

    @property
    def err_value(self) -> E:
        if self._is_ok:
            raise RuntimeError("結果がokの場合はerr_valueにアクセスしないでください")
        assert not isinstance(self._err_value, _Nil)
        return self._err_value

    def map[U](self, f: Callable[[T], U]) -> _Result[U, E]:
        if self.is_ok:
            return _Result.ok(f(self.ok_value))
        return _Result.err(self.err_value)

    def map_err[F](self, f: Callable[[E], F]) -> _Result[T, F]:
        if self.is_err:
            return _Result.err(f(self.err_value))
        return _Result.ok(self.ok_value)

    def and_then[U](self, f: Callable[[T], _Result[U, E]]) -> _Result[U, E]:
        if self.is_ok:
            return f(self.ok_value)
        return _Result.err(self.err_value)

    def ok_value_or(self, default: T) -> T:
        if self.is_ok:
            return self.ok_value
        return default

    def ok_value_or_else(self, f: Callable[[E], T]) -> T:
        if self.is_ok:
            return self.ok_value
        return f(self.err_value)

    def expect(self, msg: str) -> T:
        """Okならok_valueを返し、Errならmsgを含むAssertionErrorを発生させる"""
        assert self.is_ok, f"[Unexpected _Result Status] {msg}: {self.err_value}"
        return self.ok_value
