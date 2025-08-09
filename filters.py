from functools import partial
from typing import Any, Callable, Iterator

from models import LogRecord


class FilterPipeline:
    """Создает пайплайн из фильтров.

    Фильтры добавляются через один из методов add.
    Метод add_equal добавляет в пайплайн фильтр по
    значению атрибута key, он проверяется на равенство
    значению value.
    На данный момент add_equal не используется,
    но может быть использован в дальнейшем для расширения
    возможностей фильтрации.
    Метод add_contains добавляет в пайплайн фильтр по
    значению атрибута key, он проверяется на вхождение value
    в значение атрибута key.
    Метод apply применяет все переданные в пайплайн фильтры
    к итератору и возвращает итератор.
    """

    def __init__(self) -> None:
        self._filters: list[Callable[[LogRecord], bool]] = []

    @staticmethod
    def _equal(log: LogRecord, key: str, value: Any) -> bool:
        return getattr(log, key) == value

    @staticmethod
    def _contains(log: LogRecord, key: str, value: Any) -> bool:
        return value in (getattr(log, key) or "")

    def add_equal(self, key: str, value: Any) -> None:
        self._filters.append(partial(self._equal, key=key, value=value))

    def add_contains(self, key: str, value: Any) -> None:
        self._filters.append(partial(self._contains, key=key, value=value))

    def apply(self, logs: Iterator[LogRecord]) -> Iterator[LogRecord]:
        for f in self._filters:
            logs = filter(f, logs)
        yield from logs
