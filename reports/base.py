from abc import ABC, abstractmethod
from typing import Any, Iterator

from tabulate import tabulate

from models import LogRecord


class Report(ABC):
    """Абстрактный класс отчета.

    Интерфейс классов отчетов.
    При инициализации экземпляра на вход принимается итератор из
    логов и заголовки отчета.
    Метод print лениво генерирует отчет при вызове и кеширует его
    в атрибуте self._rows, а затем печатает отчет.
    В наследниках класса необходимо переопределить _generate и
    присвоить значение self._headers (например в методе __init__).
    """

    def __init__(
        self, logs: Iterator[LogRecord], headers: tuple[str, ...] = tuple()
    ) -> None:
        self._logs = logs
        self._headers = headers
        self._rows: tuple[tuple[Any, ...], ...] | None = None

    @abstractmethod
    def _generate(self) -> tuple[tuple[Any, ...]]: ...  # noqa: E704

    def print(self) -> None:
        if self._rows is None:
            self._rows = self._generate()
        print(tabulate(self._rows, headers=self._headers))
